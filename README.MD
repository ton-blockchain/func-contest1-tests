# Setup
Install python, tar, [update toncli to 0.0.33 version](https://github.com/disintar/toncli) and update toncli libs (`toncli update_libs`).

# Run tests
Put `tar` archive which you submitted to bot into submitions directory.

Run `python checker.py`.

Results (scores) will be written to `results.csv`. 

You can also run tests manually:
  * Put `*.fc` to `tests/func`
  * `cd tests`
  * `toncli run_tests -c contest-1 -o`
  * `toncli run_tests -c contest-2 -o`
  * `toncli run_tests -c contest-3 -o`
  * `toncli run_tests -c contest-4 -o`

It will write to console which tests you passed.

Note, that contest-5 is a little bit different. In addition to all tests required to be passed, it also requires that for all tests in the `["get_one_ext_message", "get_coupled_ext_message", "first_sign_1", "first_sign_2", "first_sign_3", "second_sign_4", "first_cosign_1", "second_cosign_2", "mass_first_sign_1", "mass_first_sign_2", "mass_first_sign_3", "mass_second_sign_4", "mass_second_sign_5", "mass_second_sign_6", "mass_second_sign_7_251", "mass_second_sign_8_251", "mass_second_sign_9_77", "mass_first_cosign_9_77", "mass_second_sign_10_77", "mass_second_sign_11_77", "mass_second_sign_12_77", "mass_second_sign_13_77", "mass_second_sign_14_77", "mass_second_sign_15_77", "mass_second_sign_16_251", "mass_first_cosign_16_251"]` list `gas_limit` will me equal to `max_gas_limit` (in other words message was _accepted_). And for all tests in `["second_cosign_2_replay", "second_sign_4_replay", "second_sign_1_too_late", "second_sign_7_too_late", "wrong_sign_body", "mixed_sign_body", "wrong_key_body", "no_msg_body", "incorrect_request_body", "incorrect_layout_body"]` message should not be accepted (`gas_limit == 10000`).


# Acknowledgements
@tvorogme and [disintar team](https://github.com/disintar) for helping in organization of easy to use test suite.
