from redisai import Client

REDIS_HOST = "172.20.0.20"
REDIS_PORT = 6379

rai_client = Client(host=REDIS_HOST, port=REDIS_PORT)

def get_loan_prediction(
        dob_ssn: str,
        zipcode: str,
        age: int,
        income: int,
        emp_length: int,
        loan_amount: int,
        int_rate: float,
        script_key: str,
        model_key: str
    ):

    keys = [dob_ssn, zipcode]
    input_args = [str(x) for x in [age, income, emp_length, loan_amount, int_rate]]
    out_tag = hash(dob_ssn)

    dag = rai_client.dag(persist=[f"out_1_{out_tag}", f"out_2_{out_tag}"])
    dag.scriptexecute(script_key, 'enrich_features', keys=keys, args=input_args, outputs=['model_input'])
    dag.modelexecute(model_key, inputs=['model_input'], outputs=[f'out_1_{out_tag}', f"out_2_{out_tag}"])
    dag.execute()

    score = rai_client.tensorget(f'out_1_{out_tag}')
    probabilities = rai_client.tensorget(f"out_2_{out_tag}")
    return score, probabilities
