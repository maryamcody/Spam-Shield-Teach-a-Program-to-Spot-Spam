# Step 1: spam words znd how  "spammy" each one is (its weight)
SPAM_WORDS= {
    "free":2, "winner":3, "won":3, "prize":3, "lottery":3,
    "urgent":2, "click":2, "claim":2 , "cash":2, "verify":2,
    "congratulations":2, "offer":1, "limited":1, "now":1, "account":1,

}
THERSHOLD= 4 #a score at or above this means Spam
USE_LEFT= False # "Break it" step: set to True to catch WINNER, click, prize

LEFT= str.maketrans("13450@$", "ieasoas") #1->i, 3->e, 4->a,5->s,0->o, @->a,$->s
PUNCTUATION =".,!?:;\"'()"

# Step 2: Clean one word, then split a message into clean words

def  clean_word(word):
    word = word.lower()
    if USE_LEFT:
        word= word.translate(LEFT)
    return word.strip(PUNCTUATION)


def tokenize(message):
    words=[]
    for word in  message.split():
        cleaned = clean_word(word)
        if cleaned:
            words.append(cleaned)
    return words


# step 3: Add up the weights of everyspamword in the message
def spam_score(message):
    score = 0
    for word in tokenize(message):
        score += SPAM_WORDS.get(word, 0)
    return score

# Step 4 : DEcide Spam OR SAFE , and explain which words were flagged
def classify(message):
    if spam_score(message)>= THERSHOLD:
        return "SPAM"
    return "SAFE"

def explain(message):
    return [word  for word in tokenize(message)if word in SPAM_WORDS]

# Step 5 : Test on messages where we are already know the right answer

TEST_MESSAGES = [

("Congratulations! You WON a free iPhone. Click now to claim", "SPAM"),

("URGENT: verify your account or it will be blocked", "SPAM"),

("Claim your cash prize before midnight", "SPAM"),

("Hey, are we still meeting at 5?", "SAFE"),

("Your free coding class starts at 5 PM today", "SAFE"),

("Mom says dinner is ready, come down now", "SAFE"),

("W1NNER!!! cl1ck here for your pr1ze", "SPAM"),

("Limited offer: free cash for new users, claim now", "SPAM"),

("Click the link in the class group to join the free quiz now", "SAFE"),

("Your bank account statement for March is ready", "SAFE"),

]


def run_tests():
    correct = false_positives = false_negatives = 0
    for message, expected in TEST_MESSAGES:
       result = classify(message)
       if result == expected:
           correct += 1
           mark = "OK"
       elif result =="SPAM":
           false_positives +=1
           mark = "FP" #  a safe message wrongly blocked
       else:
           false_negatives += 1
           mark ="FN" ##  spam that slipped throurgh
       print(f"{mark} {result} score={spam_score(message):>2} {message}")
       print(f"\nAccuracy: {correct}/{len(TEST_MESSAGES)}")
       print(f"False positives (safe messages blocked):{false_positives}")
       print(f"False negatives (spam that goy through):{false_negatives}")


if __name__=="__main__":
    run_tests()
    print("\nType a message to check it , or 'quit' to stop.")
    while True:
        message = input("\n>")
        if message.strip().lower() == "quit":
            break
        print(f"{classify(message)} | score: {spam_score(message)} | flagged: {explain(message)}")

          
       
 