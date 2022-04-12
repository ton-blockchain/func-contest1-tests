import os
import json
import math

s_path = 'submitions'
submitions = [os.path.join(s_path, f) for f in os.listdir(s_path) 
                  if ( os.path.isfile(os.path.join(s_path, f)) and len(f)>4 and f[-4:] == ".tar")]

print(submitions)

def untar(solution_path):
  os.system('tar -xf %s -C current_solution/'%solution_path)

def find_solutions():
  all_files = []
  for dirpath, dirnames, filenames in os.walk("current_solution/"):
    all_files += [os.path.join(dirpath,f) for f in filenames]
  result = {}
  for s in ["1.fc", "2.fc","3.fc", "4.fc", "5.fc", "out", "participant.json"]:
    result[s] = None
    # lets combat upper/lower cases in dumb way
    for i in all_files:
      if s.lower() in i.lower():
        if result.get(s):
          if len(result.get(s)) > len(i):
            result[s] = i
        else:
          result[s] = i
  return result
 
def move_solution(path):
  os.system('cp %s tests/func/'%path)
  
def score(success, gas_usage, etalon):
  #print( " + ".join([ str(i) for i in gas_usage.values()]))
  if not success:
    return 0
  else:
    total_gas = sum(gas_usage.values())
    return 5 + math.exp(- float(total_gas)/etalon)

def check(path, name, etalon_gas, measured, external = False, non_accepted = []):
  if not path:
    return 0
  move_solution(path)
  os.system("cd tests; toncli run_tests -c %s -o;"%name)
  res = False
  gas_usage = {}
  try:
    processed = {}
    with open("tests/tests_output.json", "r") as f:
      raw = f.read()
      processed = json.loads(raw)["tests"]
    for j in measured:
      gas_usage[j] = -1
    res = True
    for i in processed:
      res = res and (i["exit_code"] == 0)
      if i["name"] in measured:
          gas_usage[i["name"]] = i["gas_used"]
      if external:
        if i["name"] in non_accepted:
          res = res and (not (i["gas_limit_vm"] == i["gas_max_vm"]))
        else:
          res = res and (i["gas_limit_vm"] == i["gas_max_vm"])
  except Exception as e:
    print(e)
    return 0
  os.system("rm tests/tests_output.json")
  return score(res, gas_usage, etalon_gas)
  
def check_1(path):
  etalon_gas = 566 + 1127 + 1127 + 1127 + 1127 + 1127 + 1127
  measured = ["not_valid", "add_10", "second_add_10", "third_add_10", "add_64", "add_max_32", "add_max_32_twice"]
  return check(path, "contest-1", etalon_gas, measured)

def check_2(path):
  etalon_gas = 3420 + 1481;
  measured = ["valid", "message_from_owner"]
  return check(path, "contest-2", etalon_gas, measured)

def check_3(path):
  etalon_gas = 2199 + 3324 + 1305;
  measured = ["manager_set_address", "request_address", "unvalid_message"]
  return check(path, "contest-3", etalon_gas, measured)

def check_4(path):
  etalon_gas = 4530 + 6668 + 6746 + 6746 + 8467 + 9267 + 7946 + 10268 + 8393 + 5142 + 6492 + 6492 + 4930 + 16991 + 37905 + 6746 + 7346 + 7946 + 8546 + 8546 + 8546 + 9146 + 9746 + 9146 + 8546 + 8468 + 12668 + 12668 + 12668 + 12668 + 12668 + 12668 + 12668 + 9668 + 4546;
  measured = ["set_message", "set_message_2", "set_message_3", "set_message_4", "set_message_same_valid_until", "set_message_same_value", "set_message_update_valid_until_before", "set_message_update_valid_until", "set_message_update_valid_until_again", "remove_outdated", "remove_outdated2", "remove_outdated3", "remove_outdated4", "remove_outdated5", "remove_outdated6", "mass_key_addition1", "mass_key_addition2", "mass_key_addition3", "mass_key_addition4", "mass_key_addition5", "mass_key_addition6", "mass_key_addition7", "mass_key_addition8", "mass_key_addition9", "mass_key_addition10", "mass_key_addition11", "mass_key_addition12", "mass_key_addition13", "mass_key_addition14", "mass_key_addition15", "mass_key_addition16", "mass_key_addition17", "mass_key_addition18", "mass_key_addition110", "add_outdated_but_not_removed"]
  return check(path, "contest-4", etalon_gas, measured)

def check_5(path):
  etalon_gas = 4187 + 4788 + 4187 + 6037 + 6662 + 6662 + 6763 + 8013 + 4187 + 6037 + 6662 + 6662 + 7287 + 7287 + 7912 + 7287 + 7912 + 8013 + 7912 + 8537 + 28471 + 6037 + 6662 + 7287 + 7287 + 7388;
  measured = ["get_one_ext_message", "get_coupled_ext_message", "first_sign_1", "first_sign_2", "first_sign_3", "second_sign_4", "first_cosign_1", "second_cosign_2", "mass_first_sign_1", "mass_first_sign_2", "mass_first_sign_3", "mass_second_sign_4", "mass_second_sign_5", "mass_second_sign_6", "mass_second_sign_7_251", "mass_second_sign_8_251", "mass_second_sign_9_77", "mass_first_cosign_9_77", "mass_second_sign_10_77", "mass_second_sign_11_77", "mass_second_sign_12_77", "mass_second_sign_13_77", "mass_second_sign_14_77", "mass_second_sign_15_77", "mass_second_sign_16_251", "mass_first_cosign_16_251"]
  non_accepted = ["second_cosign_2_replay", "second_sign_4_replay", "second_sign_1_too_late", "second_sign_7_too_late", "wrong_sign_body", "mixed_sign_body", "wrong_key_body", "no_msg_body", "incorrect_request_body", "incorrect_layout_body"]
  return check(path, "contest-5", etalon_gas, measured, True, non_accepted)
  

def clean_up():
  os.system('rm -rf current_solution/* current_solution/.??* ; rm tests/func/* tests/func/.??* ;');


def show_results(results, presence):
  for i,r in enumerate(results):
    print("Task {0}:\tsubmitted {1: >5},\taccepted {2: >5},\tscore:{3: .2f}".format(i+1, str(presence[i]), str(results[i]>5), results[i]))
  print("Total score: %.2f"%sum(results))
    

def check_all():
  with open("result.csv", "w") as f:
    f.write("Archive, score, address, username, codeforces, out, score1, score2, score3, score4, score5, exist1, exist2, exist3, exist4, exist5\n")  
  for submition in submitions[:]:
    print(submition)
    untar(submition)
    solutions = find_solutions()
    print(solutions)
    results = []
    presence = []
    results.append(check_1(solutions['1.fc']))
    results.append(check_2(solutions['2.fc']))
    results.append(check_3(solutions['3.fc']))
    results.append(check_4(solutions['4.fc']))
    results.append(check_5(solutions['5.fc']))
    for i in range(1,6):
      presence.append(bool(solutions[str(i)+".fc"]))
    participant ={}
    try:
      print(solutions['participant.json'])
      with open(solutions['participant.json'], "r") as f:
        have = f.read()
        print(have)
        participant = json.loads(have)
    except Exception as e:
      print(submition)
      raise e
    show_results(results, presence)
    total = [submition, sum(results), participant.get("address"), participant.get("username"), participant.get("codeforces")] +\
            [solutions["out"]]+\
            results+\
            presence;
    with open("result.csv", "a+") as f:
      f.write(", ".join([str(i) for i in total])+"\n")
    #print(submition, result2)
    clean_up()

check_all()


