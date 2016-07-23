// Huajie uiuc @2016/7/20
// Tanvir Amin
// UIUC
// February 2014

// Dong Wang
// UIUC
// May 2011

#include "matrix.h"

#include <algorithm>
#include <cfenv>
#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <iostream>
#include <map>
#include <memory>
#include <time.h>
#include <string>
#include <sstream>
#include <unordered_map>

using std::ifstream;
using std::map;
using std::string;
using std::vector;
using std::unordered_map;
using std::pair;
using std::stringstream;

//#define T 1000
//#define F 1000
//#define nSources 50


// SPECIAL: DEFAULT EM_ITER IS 20, CHANGED TO 5 FOR SPEED
// #define EM_ITER 5
#define EM_ITER 20
#define BOUND_95 1.96
#define BOUND_90 1.64
#define BOUND_68 1.00
#define EPS 1e-12

typedef pair<long long, double> my_pair;

bool SortScore (const my_pair& left, const my_pair& right) {
  return ( left.second > right.second );
}

void WriteIntermediateResults(string &cluster_cred, int iter,
    vector<long long> &Assertion,
    vector<double> &Z) {
  FILE *fp2;
  int j;
  string s = cluster_cred + "." + std::to_string(iter);
  if (!(fp2 = fopen(s.c_str(), "w")))
    std::cerr << "Temporary file open failed: No data saved on file!\n";

  for (j=0; j < Assertion.size(); j++){
    fprintf(fp2, "%lld\t %.5f\n", Assertion[j], Z[j]);
  }
  fclose(fp2);
}

void InputSourceClaims(ifstream& input,
    vector<long long>& Source,
    vector<long long>& Source_All,
    vector<long long>& Assertion,
    vector<long long>& Assertion_All) {
  string line;
  size_t line_index;
  while(getline(input,line)){
    line_index=0;
    while (line[line_index] != '\0' && line_index < 10000) {
      char str[1000];
      size_t str_index = 0;
      while ((line[line_index] != '\t') && (line[line_index] != '\0')
          && (str_index < 1000))
        str[str_index++] = line[line_index++];
      str[str_index] = '\0';

      if (line[line_index] == '\t'){
        line_index++;
        Source_All.push_back(atoll(str));
        Source.push_back(atoll(str));
      }
      if (line[line_index] == '\0'){
        Assertion_All.push_back(atoll(str));
        Assertion.push_back(atoll(str));
      }
    }
  }
}

void InputSourcePriors(ifstream& input,
    unordered_map<long long, std::shared_ptr<vector<double>>>& sourcePriors) {
  string line;
  while (getline(input, line)) {
    stringstream valuestream(line);
    long long sourceId;
    auto values = std::make_shared<vector<double>>(2);
    valuestream >> sourceId >> (*values)[0] >> (*values)[1] ;
    sourcePriors[sourceId] = values;
  }
}

void print_usage_and_abort() {
  std::cerr << "Usage: EM-Social-Checkpoint \
    input_file \
    social_file \
    d_initial \
    source_prob_file \
    cluster_prob_file \
    source_conf_file \
    [soure_prior_file] no use" << std::endl;
  exit(-1);
}

int main(int argc, char** argv) {
  // enable floating point exception
  feenableexcept(FE_DIVBYZERO | FE_INVALID | FE_OVERFLOW);

  int MIN_ARGS = 7;  // Minimum arguments that are required
  if (argc < MIN_ARGS) {
    print_usage_and_abort();
  }

  /*
  // print parameters
  std::cerr << "Parameters: ";
  for (int i = 0; i < argc; i++)
    std::cerr << argv[i] << " ";
  std::cerr << std::endl;
  */

  int nSources, nClaims;

  vector <double> PSI, PSI_ET, ERR_S;
  vector <int> LI;
  vector <long long> id_src_list, nd_src_list, all_rec_src_list;
  vector <double> Claim;
  vector <double> si_init, a_em, b_em, t_em, Z, std_t_em, up_t_em, low_t_em;
  vector <double> TRUE_ASSERT, FALSE_ASSERT;

  int i = 0, j = 0, k = 0, n = 0;
  int claim_true_id = -1, claim_false_id = -1;
  double source_min = 0, bound_factor = 0;
  double d_em = 0, sum_em = 0;
  double left_sum=0, right_sum = 0;
  double A_in = 0, A_out = 0;
  double K_i = 0, K_n = 0, K_d = 0;
  double A_n = 0, A_d = 0;
  double err_avg = 0, false_positive = 0, false_negative = 0;

  FILE * fp1;
  FILE * fp2;
  FILE * fp0;

  string line;
  vector <long long> Source_All, Assertion_All;
  vector <long long> Source, Assertion;
  vector <long long>::iterator newS, newA, newall;
  size_t line_index;
  //To do: make SrcDep: long long and vector<long long>
  map <long long, vector <long long> > SrcDep, SrcDepIndex;
  map <long long, long long> SrcIndepbinary;
  map <long long, vector <double> > pg;

  ifstream input(argv[1]);
  ifstream input2(argv[2]);

  // Read source claim graph.
  if (!input) {
    std::cerr << "Invalid Source-Claim file. Aborting." << std::endl;
    return 2;
  }
  else {
    std::cerr << "Loading Source-Claim network." << std::endl;
    InputSourceClaims(input, Source, Source_All, Assertion, Assertion_All);
    input.close();
  }

  //Get Unique Source and Assertion
  sort(Source.begin(), Source.end());
  sort(Assertion.begin(), Assertion.end());
  newS = unique(Source.begin(),Source.end());
  newA = unique(Assertion.begin(), Assertion.end());
  Source.erase(newS, Source.end());
  Assertion.erase(newA, Assertion.end());

  nSources = Source.size();
  nClaims = Assertion.size();

  std::cerr << "Sources: " << nSources << " Assertions: " << nClaims << std::endl;

  //Give rough estimate of d_em here
  d_em = atof(argv[3]);
  if (d_em <= 0)
    d_em = 0.5;

  string source_prob_output = argv[4];
  string cluster_prob_output = argv[5];
  string source_conf_output = argv[6];

  // map to store source priors (inital values of ai, bi)
  unordered_map<long long, std::shared_ptr<vector<double>>> sourcePriors;

  // read priors (if given)
  if (argc > MIN_ARGS) {
    ifstream prior_file(argv[MIN_ARGS]);
    if (!prior_file)
      std::cerr << "Prior file not present." << std::endl;
    else {
      std::cerr << "Loading priors." << std::endl;
      InputSourcePriors(prior_file, sourcePriors);
      prior_file.close();
    }
  }

  long long nd_src = 0;
  long long id_src = 0;

  if (!input2)
    std::cerr << "Source-Dependency file not present." << std::endl;
  else {
    line_index=0;

    std::cerr << "Loading Source-Dependency network." << std::endl;
    while(getline(input2,line)) {
      line_index = 0;
      while (line[line_index] != '\0' && line_index < 10000) {
        char str[1000];
        size_t str_index = 0;
        string str1;

        while ((line[line_index] != ',') && (line[line_index] != '\0')
            && (str_index < 1000))
          str[str_index++] = line[line_index++];
        str[str_index] = '\0';

        if (line[line_index] == ','){
          line_index++;
          nd_src=atoll(str);
          nd_src_list.push_back(nd_src);

        }
        if (line[line_index] == '\0'){
          id_src=atoll(str);
          SrcDep[nd_src].push_back(id_src);
          id_src_list.push_back(id_src);
        }
      }
    }
    input2.close();
  }

  all_rec_src_list.insert(all_rec_src_list.end(),
      id_src_list.begin(), id_src_list.end());
  all_rec_src_list.insert(all_rec_src_list.end(),
      nd_src_list.begin(), nd_src_list.end());
  sort(all_rec_src_list.begin(), all_rec_src_list.end());
  newall = unique(all_rec_src_list.begin(),all_rec_src_list.end());
  all_rec_src_list.erase(newall, all_rec_src_list.end());

  std::cerr << "Sources in Dependency File: " << all_rec_src_list.size()<<std::endl;

  // Create the source claim matrix CS
  Matrix CS(nClaims, nSources);
  for(j = 0; j < nClaims; j++) {
    for (i = 0; i < nSources; i++) {
      CS.set(j, i, 0);
    }
  }

  size_t assertion_index=0;
  size_t source_index=0;

  for(i=0; i < Assertion_All.size(); i++) {
    for(assertion_index = 0; assertion_index < Assertion.size(); assertion_index++){
      if(Assertion[assertion_index] == Assertion_All[i])
        break;
    }
    for(source_index = 0; source_index < Source.size(); source_index++){
      if(Source[source_index] == Source_All[i])
        break;
    }
    if (CS.get(assertion_index, source_index)==0)
      CS.set(assertion_index, source_index, 1);
  }


  //Build SrcDepIndex Map, SrcIndepBinary


  long long src_id = 0;
  long long leader_id = 0;
  long long leader_index = 0;

  std::cerr << "Build SrcDepIndex Map, SrcIndepBinary..." << std::endl;

  int cnt=0;
  for (i = 0; i < nSources; i++){
    src_id = Source[i];
    if (find(nd_src_list.begin(), nd_src_list.end(), src_id)
        == nd_src_list.end()) {
      SrcIndepbinary[src_id] = 1;
    }

    else{
      for(j = 0; j != SrcDep[src_id].size(); j++) {
        leader_id = SrcDep[src_id][j];
        for(source_index = 0; source_index < Source.size(); source_index++) {
          if(Source[source_index]==leader_id)
            break;
        }
        leader_index=source_index;
        SrcDepIndex[src_id].push_back(leader_index);
      }

      SrcIndepbinary[src_id] = 0;
    }
  }

  //--------------------------------------------

  //EM algorithm
  std::cerr << "EM is Initializing..." << std::endl;

  for(i = 0; i < nSources; i++) {
    //Initialize pg;
    long long src_id = Source[i];
    double dep_claim = 0;
    vector <long long> dep_claim_list;

    //Independent leader
    if (SrcIndepbinary[src_id] == 1) {
      pg[src_id].push_back(0);
    } else {
      //Non-independent member;
      for (j = 0; j != SrcDepIndex[src_id].size(); j++) {
        long long leader_index = SrcDepIndex[src_id][j];

        //Figure out how many claims both i and his leader claimed->P_n
        //Figure out how many claims only the leader claimed->P_d
        double P_n = 0;
        double P_d = 0;
        //  double P_i=0;
        //User source and leader index to access CS array
        for(int j1 = 0; j1 < nClaims; j1++) {
          if  (CS.get(j1,i) == 1 && CS.get(j1,leader_index) == 1) {
            P_n = P_n + 1;
            if (find(dep_claim_list.begin(), dep_claim_list.end(), j1)
                == dep_claim_list.end()) {
              dep_claim_list.push_back(j1);
              dep_claim = dep_claim + 1;
            }
          }
          if (CS.get(j1,leader_index) == 1) {
            P_d = P_d + 1;
          }
        }
        pg[src_id].push_back(P_n / P_d);

      }
    }

    //Initialize s_i

    double li = 0;
    double si = 0;
    double dep_spk;

    for(j = 0;j < nClaims; j++){
      li = li + CS.get(j,i);
    }
    si = li / nClaims;
    dep_spk = dep_claim / li;
    si_init.push_back(si * (1 - dep_spk));

  }

  // Initialize ai, bi
  for (i = 0; i < nSources; i++) {
    // is this source present in source priors
    auto found = sourcePriors.find(Source[i]);
    if (found == sourcePriors.end()) {  // initialize from speak rate
      a_em.push_back(si_init[i]);
      b_em.push_back(si_init[i] * 0.5);
    } else {  // initialize from priors
      a_em.push_back(found->second->at(0));
      b_em.push_back(found->second->at(1));
    }
    t_em.push_back(0);
    std_t_em.push_back(0);
    up_t_em.push_back(0);
    low_t_em.push_back(0);

  }

  // Initialize zi
  for (i = 0; i < nClaims; i++){
    Z.push_back(-1);
  }

  //return 0;

  std::cerr<<"EM is Iterating..."<<std::endl;

  //EM Iterate
  for (n = 0; n < EM_ITER; n++) {
    std::cerr << "Writing Intermediate Results ... ";
    WriteIntermediateResults(cluster_prob_output, n, Assertion, Z);
    std::cerr << "Starting Iteration " << n + 1 << std::endl;


    // Update Z
    for(j = 0;j < nClaims; j++){

      left_sum=0;
      right_sum=0;

      for(i = 0; i < nSources; i++){
        if(a_em[i] > 0.9999){
          //  std::cerr<<"a_em==1"<<std::endl;
          a_em[i] = 0.9999;
        }
        else if (a_em[i] < 0.0001){
          //std::cerr<<"a_em==0"<<std::endl;
          a_em[i] = 0.0001;
        }
        else{;}
        if(b_em[i] > 0.9999){
          //  std::cerr<<"b_em==1"<<std::endl;
          b_em[i] = 0.9999;
        }
        else if (b_em[i] < 0.0001){
          //  std::cerr<<"b_em==0"<<std::endl;
          b_em[i] = 0.0001;
        }
        else{;}

        //Indpendent leader 
        long long src_id = Source[i];
        if (SrcIndepbinary[src_id]==1){
          left_sum = left_sum + CS.get(j,i) * log(a_em[i])
            + (1 - CS.get(j,i)) * log(1-a_em[i]);
          right_sum = right_sum + CS.get(j,i) * log(b_em[i])
            + (1 - CS.get(j,i)) * log(1 - b_em[i]);

        }

        //Non-Independent member, partially follow
        else{
          for (int h=0; h != SrcDepIndex[src_id].size(); h++){
            leader_index = SrcDepIndex[src_id][h];

            // Non-independent member who don't follow their leader
            if (pg[src_id][h]==0) {
              if (CS.get(j,leader_index)==1) {
                //    left_sum=0;
                //    right_sum=0;
                continue;
              }
              //If leader does not say the claim, members are independet to claim it
              else{
                left_sum = left_sum + CS.get(j, i) * log(a_em[i])
                  + (1 - CS.get(j, i)) * log(1 - a_em[i]);
                right_sum = right_sum + CS.get(j,i) * log(b_em[i])
                  + (1 - CS.get(j, i)) * log(1 - b_em[i]);
                //return 0;
              }
            }
            // Non-independent member who do partially follows what the leader said
            else{
              if (pg[src_id][h] == 1){
                left_sum = left_sum + CS.get(j, leader_index) * (CS.get(j, i) * log(pg[src_id][h])) + (1 - CS.get(j,leader_index)) * (CS.get(j,i) * log(a_em[i]) + (1 - CS.get(j,i)) * log(1 - a_em[i]));
                right_sum = right_sum + CS.get(j,leader_index) * (CS.get(j,i) * log(pg[src_id][h])) + (1 - CS.get(j,leader_index)) * (CS.get(j,i) * log(b_em[i]) + (1 - CS.get(j,i)) * log(1 - b_em[i]));
              }
              else if (pg[src_id][h] == 0)
              {
                left_sum = left_sum + CS.get(j,leader_index) * ((1 - CS.get(j,i)) * log(1 - pg[src_id][h])) + (1 - CS.get(j,leader_index)) * (CS.get(j,i) * log(a_em[i])+(1-CS.get(j,i)) * log(1-a_em[i]));
                right_sum = right_sum + CS.get(j,leader_index) * ((1 - CS.get(j,i)) * log(1 - pg[src_id][h])) + (1 - CS.get(j,leader_index)) * (CS.get(j,i) * log(b_em[i]) + (1 - CS.get(j,i)) * log(1 - b_em[i]));
              }
              else{
                left_sum=left_sum+CS.get(j,leader_index)*(CS.get(j,i)*log(pg[src_id][h])+(1-CS.get(j,i))*log(1-pg[src_id][h]))+(1-CS.get(j,leader_index))*(CS.get(j,i)*log(a_em[i])+(1-CS.get(j,i))*log(1-a_em[i]));
                right_sum=right_sum+CS.get(j,leader_index)*(CS.get(j,i)*log(pg[src_id][h])+(1-CS.get(j,i))*log(1-pg[src_id][h]))+(1-CS.get(j,leader_index))*(CS.get(j,i)*log(b_em[i])+(1-CS.get(j,i))*log(1-b_em[i]));
              }
            }
          }
        }

      }


      if(d_em > 0.9999){
        d_em = 0.9999;
        //  std::cerr<<"d_em==1"<<std::endl;
      }
      else if(d_em < 0.0001){
        d_em = 0.0001;
        //  std::cerr<<"d_em==0"<<std::endl;
      }
      else {;}

      // Calculate new value of Z[j]
      Z[j] = 1 / (1 + exp(right_sum - left_sum + log((1 - d_em) / d_em)));

    }

    //Update d_em
    sum_em = 0;
    for(j = 0; j < Z.size(); j++){
      sum_em = sum_em + Z[j];
    }
    d_em = sum_em/(double)Z.size();

    //Update a_em and b_em

    for (i=0; i<nSources; i++) {
      A_in=0;
      A_out=0;
      K_i=0;
      K_d=0;
      K_n=0;
      A_d=0;
      A_n=0;

      long long src_id = Source[i];

      //Indpendent leader
      if (SrcIndepbinary[src_id]==1) {
        for (j = 0; j < nClaims; j++) {
          if(CS.get(j,i) == 1) {
            K_i = K_i + 1;
            A_in = A_in + Z[j];
          } else {
            A_out = A_out + Z[j];
          }
        }
        // new value of ai and bi for independent member
        a_em[i] = A_in / (A_in + A_out);
        b_em[i] = (double)(K_i - A_in) / (double)(nClaims - A_in - A_out);
      } else {  //Non-Independent member
        int leader_flg=0;

        for (j=0; j < nClaims; j++){
          //Check if any of my parent claimed j or not
          for (int h = 0; h != SrcDepIndex[src_id].size(); h++) {
            leader_index = SrcDepIndex[src_id][h];
            if (CS.get(j,leader_index) == 1) {
              leader_flg = 1;
              break;
            }
          }

          if (leader_flg == 0) {
            K_d = K_d + 1;
            A_d = A_d + Z[j];
            if (CS.get(j,i) == 1) {
              K_n = K_n + 1;
              A_n = A_n + Z[j];
            }
          }
          leader_flg = 0;
        }

        // new value of ai and bi for non independent member
        a_em[i] = A_n / A_d;
        // fixing floating point exception
        double ka = K_n - A_n;
        if (fabs(ka) < EPS) {
          b_em[i] = 0.0;
        } else {
          b_em[i] = (K_n - A_n) / (K_d - A_d);
        }

      }

      //no_independent claim, indpendent reliability is o
      if (si_init[i] == 0) {
        t_em[i] = 0;
      } else {
        t_em[i] = d_em * (a_em[i]) / (d_em * (a_em[i]) + (1-d_em) * (b_em[i])); 
      }
    }
  }  //End of EM Iterate

  // -------------------------------------------------
  // add the text files to save ai and bi by Huajie @7/20/2016
  // -------------------------------------------------
  std::ofstream a_rst ("ai_rst.txt", std::ios::out);
  std::ofstream b_rst ("bi_rst.txt", std::ios::out);
  // int len_a =sizeof(a_em)/sizeof(a_em[0]);
  for (int i=0; i<nSources;i++)
  {
    a_rst << a_em[i]<< "\r\n";   // this is very improtant
    b_rst << b_em[i]<< "\r\n";
  
  }
  a_rst.close();
  b_rst.close();
  
  // ----------------------------------------------
  bound_factor=BOUND_90;
  // bound_factor=BOUND_95;

  //Compute CRB for t_em
  for(i = 0;i < nSources; i++) {
    if (si_init[i] > 0) {  // The source made independent claims.
      std_t_em[i] = d_em / si_init[i]
        * sqrt((a_em[i] * (1 - a_em[i])) / (nClaims * d_em));
    } else {  // i.e si_init[i] = 0 because no independent claim.
      std_t_em[i] = 0;
    }

    up_t_em[i] = t_em[i] + bound_factor * std_t_em[i];
    low_t_em[i] = t_em[i] - bound_factor  *std_t_em[i];

    if(up_t_em[i] > 1) up_t_em[i] = 1;
    if(low_t_em[i] < 0) low_t_em[i] = 0;
  }



  //Output Result
  char *a1=new char[source_prob_output.size()+1];
  a1[source_prob_output.size()]=0;
  memcpy(a1,source_prob_output.c_str(),source_prob_output.size());

  char *a2=new char[cluster_prob_output.size()+1];
  a2[cluster_prob_output.size()]=0;
  memcpy(a2,cluster_prob_output.c_str(),cluster_prob_output.size());


  char *a0=new char[source_conf_output.size()+1];
  a0[source_conf_output.size()]=0;
  memcpy(a0,source_conf_output.c_str(),source_conf_output.size());


  //Open an outuptfile
  if (!(fp1 = fopen(a1, "w")))
    std::cerr<<"Output file open failed: No data saved on file"<<std::endl;

  for (i = 0; i < Source.size(); i++){
    fprintf(fp1, "%lld\t %.5f\n", Source[i], t_em[i]);

  }
  fclose(fp1);


  if (!(fp0 = fopen(a0, "w")))
    printf("Output file open failed: No data saved on file!\n");


  for (i=0; i < Source.size(); i++){
    if(si_init[i] * nClaims >= source_min
        && a_em[i] > 0 && a_em[i] < 1 && t_em[i] != 0) {
      fprintf(fp0, "%lld\t %.5f\t %.5f\t %.5f\t %2.5f\n",
          Source[i], t_em[i], low_t_em[i], up_t_em[i], si_init[i]*nClaims);
    }
  }
  fclose(fp0);


  if (!(fp2 = fopen(a2, "w")))
    printf("Output file open failed: No data saved on file!\n");

  for (j = 0; j < Assertion.size(); j++){
    fprintf(fp2, "%lld\t %.5f\n", Assertion[j], Z[j]);
  }
  fclose(fp2);

  /*


  //Sort the assertions based on cred
  //vector<pair<long long, double>> Assertion_Pair;
  vector<my_pair> Assertion_Pair;


  for (j=0; j< (int) Z.size(); j++){
  //Rember to -1 when convert to cluster id
  Assertion_Pair.push_back(std::make_pair(j+1,Z[j]));

  }

  std::stable_sort(Assertion_Pair.begin(), Assertion_Pair.end(), SortScore);


  int temp_len=(int)  Assertion_Pair.size()-1;  

  if (!(fp2=fopen(a2, "w")))
  printf("Output file open failed: No data saved on file!\n");

  for (j=0; j<(int) Assertion_Pair.size(); j++){
  //  printf("%d\t %f\t %.5f\n", Assertion_Pair[j].first, Assertion_Pair[j].second, Z[j]);
  fprintf(fp2, "%lld\t%.5f\n", Assertion_Pair[j].first-1, Assertion_Pair[j].second);
  }
  fclose(fp2);


*/

  std::cerr<<"Work Done!"<<std::endl;

  return 0;
}


