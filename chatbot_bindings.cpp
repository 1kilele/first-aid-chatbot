#include <pybind11/pybind11.h>
#include <string>
#include <unordered_map>

namespace py = pybind11;

// Simple rule-based chatbot function
std::string respond(const std::string &message) {
    // Predefined responses
    static std::unordered_map<std::string, std::string> responses = {
        {"hello", "Hi there! How can I help you?"},
        {"how are you", "I'm just a chatbot, but I'm doing fine!"},
        {"bye", "Goodbye! Have a great day!"},
        {"your name", "I'm Chatbot, your AI assistant."}
    };

    // Convert message to lowercase for case-insensitive matching
    std::string lower_message = message;
    for (char &c : lower_message) c = std::tolower(c);

    // Search for a matching response
    for (const auto &pair : responses) {
        if (lower_message.find(pair.first) != std::string::npos) {
            return pair.second;
        }
    }

    return "I don't understand. Can you rephrase?";
}

// Pybind11 module definition
PYBIND11_MODULE(chatbot, m) {
    m.doc() = "Chatbot module using Pybind11";
    m.def("respond", &respond, "Respond to a user message");
}





