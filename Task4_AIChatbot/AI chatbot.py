import re
import random
import difflib

STOPWORDS = {
    "a", "an", "the", "is", "are", "am", "to", "my", "me", "it", "of",
    "for", "in", "on", "at", "and", "or", "please",
}


class Chatbot:
    def __init__(self, name="Assistant"):
        self.name = name
        self.history = []  # list of (user_text, bot_text)

        # each intent: list of trigger phrases + list of possible responses
        self.intents = {
            "greeting": {
                "patterns": ["hello", "hi", "hey", "good morning", "good evening", "yo"],
                "responses": [
                    f"Hey there! I'm {self.name}, how can I help?",
                    "Hello! What's on your mind?",
                    "Hi! Ask me anything.",
                ],
            },
            "goodbye": {
                "patterns": ["bye", "goodbye", "see you", "exit", "quit", "later"],
                "responses": ["See you later!", "Goodbye, take care!", "Bye! Come back anytime."],
            },
            "thanks": {
                "patterns": ["thanks", "thank you", "appreciate it", "thx"],
                "responses": ["You're welcome!", "No problem at all.", "Anytime!"],
            },
            "how_are_you": {
                "patterns": ["how are you", "how you doing", "how is it going"],
                "responses": [
                    "I'm just code, but I'm running smoothly! How about you?",
                    "Doing well, thanks for asking!",
                ],
            },
            "name": {
                "patterns": ["what is your name", "whats your name", "who are you"],
                "responses": [f"I'm {self.name}, a simple rule-based chatbot.", f"Call me {self.name}."],
            },
            "capabilities": {
                "patterns": ["what can you do", "help me", "what do you do"],
                "responses": [
                    "I can chat with you, answer simple questions, and do basic math if you ask.",
                    "I understand greetings, small talk, and simple calculations. Try asking me something!",
                ],
            },
            "joke": {
                "patterns": ["tell me a joke", "make me laugh", "joke"],
                "responses": [
                    "Why do programmers prefer dark mode? Because light attracts bugs.",
                    "I'd tell you a UDP joke, but you might not get it.",
                ],
            },
        }

    # ---------------------------------------------------------- nlp bits

    def tokenize(self, text):
        text = text.lower()
        text = re.sub(r"[^a-z0-9\s]", "", text)
        words = text.split()
        return [w for w in words if w not in STOPWORDS]

    def similarity(self, a, b):
        return difflib.SequenceMatcher(None, a, b).ratio()

    def match_intent(self, user_text):
        text = user_text.lower()
        text = re.sub(r"[^a-z0-9\s]", "", text)
        tokens = set(self.tokenize(user_text))

        best_intent = None
        best_score = 0.0

        for intent_name, data in self.intents.items():
            for pattern in data["patterns"]:
                pattern_clean = re.sub(r"[^a-z0-9\s]", "", pattern.lower())

                # direct match as a whole phrase/word (not a substring of
                # a larger word, e.g. "yo" inside "your")
                if re.search(r"\b" + re.escape(pattern_clean) + r"\b", text):
                    return intent_name
                if re.search(r"\b" + re.escape(text) + r"\b", pattern_clean):
                    return intent_name

                pattern_tokens = set(self.tokenize(pattern))
                overlap = tokens & pattern_tokens

                if pattern_tokens:
                    score = len(overlap) / len(pattern_tokens)
                else:
                    score = 0.0

                # only fall back to fuzzy matching when there's no keyword
                # signal at all (helps catch typos like "helo")
                if score == 0.0:
                    score = self.similarity(text, pattern_clean) * 0.6

                if score > best_score:
                    best_score = score
                    best_intent = intent_name

        if best_score >= 0.5:
            return best_intent
        return None

    # -------------------------------------------------------------- math

    def try_math(self, user_text):
        # only handle simple expressions like "2 + 2" or "what is 5 * 3"
        match = re.search(r"([-+]?\d+(\.\d+)?)\s*([\+\-\*/])\s*([-+]?\d+(\.\d+)?)", user_text)
        if not match:
            return None

        left = float(match.group(1))
        op = match.group(3)
        right = float(match.group(4))

        try:
            if op == "+":
                result = left + right
            elif op == "-":
                result = left - right
            elif op == "*":
                result = left * right
            elif op == "/":
                result = left / right
        except ZeroDivisionError:
            return "can't divide by zero"

        if result == int(result):
            result = int(result)
        return f"That equals {result}"

    # ---------------------------------------------------------- response

    def respond(self, user_text):
        user_text = user_text.strip()
        if not user_text:
            reply = "Say something and I'll try to respond!"
            self.history.append((user_text, reply))
            return reply

        math_answer = self.try_math(user_text)
        if math_answer:
            self.history.append((user_text, math_answer))
            return math_answer

        intent = self.match_intent(user_text)
        if intent:
            reply = random.choice(self.intents[intent]["responses"])
        else:
            reply = self.fallback_response(user_text)

        self.history.append((user_text, reply))
        return reply

    def fallback_response(self, user_text):
        options = [
            "I'm not sure I understand, could you rephrase that?",
            "Interesting, tell me more.",
            "I don't have an answer for that yet, try asking something else.",
            "Hmm, I didn't quite catch that.",
        ]
        return random.choice(options)


def main():
    bot = Chatbot(name="PyBot")
    print(f"{bot.name}: Hi! I'm {bot.name}. Type 'quit' anytime to leave.")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ("quit", "exit", "bye"):
            print(f"{bot.name}: {random.choice(bot.intents['goodbye']['responses'])}")
            break

        reply = bot.respond(user_input)
        print(f"{bot.name}: {reply}")


if __name__ == "__main__":
    main()
