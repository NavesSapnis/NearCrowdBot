import near_api


def overflowFix(sum):
    ONE_NEAR = 1000000000000000000000000
    ful = float(sum)*ONE_NEAR
    ful = int(ful)
    return ful


def send(key,name,to,sum):
    
    near_provider = near_api.providers.JsonProvider("https://rpc.testnet.near.org")
    sender_key_pair = near_api.signer.KeyPair(key)
    sender_signer = near_api.signer.Signer(name, sender_key_pair)
    sender_account = near_api.account.Account(near_provider, sender_signer,name)
    sum = overflowFix(sum)
    sender_account.send_money(to, sum)

send("ed25519:4eUBCs5gjmuepFH7eKbexfqRjGAM26fVQmhxC8SRyERFK8HKmo8rzxXKzomQPWkKspLzqtjCnTR3qnMnjmewfn8T","jamal_carter.testnet","someone.testnet",3.33)
