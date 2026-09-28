from client import ContractNetProtocol

def main():
    cnp = ContractNetProtocol()
    cnp.register_agent("Agent_1", 4.5)
    cnp.register_agent("Agent_2", 3.2)
    cnp.register_agent("Agent_3", 5.0)
    res = cnp.announce_and_award("Data_Ingestion_Job", 20)
    print("Contract Net Protocol Verification:")
    print(f"Task: {res['task']}")
    print(f"Winner: {res['awarded_to']} with bid {res['cost']}")

if __name__ == "__main__":
    main()
