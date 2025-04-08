
#include <pybind11/pybind11.h>
#include <string>
#include <algorithm>
#include <cctype>

namespace py = pybind11;

// Convert string to lowercase
std::string toLower(const std::string &s) {
    std::string lower = s;
    std::transform(lower.begin(), lower.end(), lower.begin(),
                   [](unsigned char c){ return std::tolower(c); });
    return lower;
}

// Expanded respond function with additional rules
std::string respond(const std::string &message) {
    std::string lower_msg = toLower(message);

    if (lower_msg == "hello" || lower_msg == "hi" || lower_msg == "hey") {
        return "Hi there! How can I help you today?";
    } else if (lower_msg == "how are you" || lower_msg == "what's up") {
        return "I'm just a program, but I'm here to help!";
    } else if (lower_msg.find("i have a question") != std::string::npos) {
        return "Sure, what's your question?";
    } else if (lower_msg == "bye" || lower_msg == "goodbye") {
        return "Goodbye! Have a great day!";
    }
    // Fallback response
    return "I'm not sure how to respond to that. Can you rephrase?";
}

PYBIND11_MODULE(chatbot, m) {
    m.doc() = "Chatbot module using Pybind11";
    m.def("respond", &respond, "Respond to a user message");
}


