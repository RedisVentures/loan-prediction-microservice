import argparse

from redisai import Client



def get_loan_prediction(dob_ssn: str, zipcode: str, age: int, income: int, emp_length: int, loan_amount: int, int_rate: float):
    keys = [dob_ssn, zipcode]
    input_args = [str(x) for x in [age, income, emp_length, loan_amount, int_rate]]
    out_tag = hash(dob_ssn)

    dag = rai_client.dag(persist=[f"out_1_{out_tag}", f"out_2_{out_tag}"])
    dag.scriptexecute(script_key, 'enrich_features', keys=keys, args=input_args, outputs=['model_input'])
    dag.modelexecute(model_key, inputs=['model_input'], outputs=[f'out_1_{out_tag}', f"out_2_{out_tag}"])
    dag.execute()

    score = rai_client.tensorget(f'out_1_{out_tag}')
    probabilities = rai_client.tensorget(f"out_2_{out_tag}")
    loan_decision = "Approved" if score[0] == 1 else "Denied"
    return loan_decision, probabilities


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Redis Server Host', type=str, default='127.0.0.1')
    parser.add_argument('-p', '--port', help='Redis Server Port', type=int, default=6379)
    args = parser.parse_args()

    rai_client = Client(host=args.host, port=args.port)

    script_key = 'get_loan_features'
    model_key = 'loan_model'


    # Example 1
    decision, prob = get_loan_prediction("19660915_3573", "24265", 23, 200000, 3, 100000, 1.3)
    print("Loan decision:", decision)
    print("Probabilities:", prob)