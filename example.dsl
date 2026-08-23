# example.dsl
# Example Multi-Agent AI Workflow DSL program
# Demonstrates: agents, tools, tasks, typed variables,
#               for-loops, if-statements, run calls, arithmetic

agent Researcher {
    tool web_search
    tool llm
    task gather(string topic) -> string data {
        action: web_search(topic)
        action: llm("summarize results")
    }
}

agent Analyzer {
    tool llm
    task sentiment(string text) -> string result {
        action: llm("detect sentiment")
    }
}

agent Writer {
    tool llm
    task compose(string summary, string tone) -> string report {
        action: llm("write a formal report")
    }
}

system {
    list topics = ["AI", "Robotics", "Security"]
    int i = 0
    bool negative_found = false
    int total = 0

    for t in topics {
        string data = run Researcher.gather(t)
        string sentiment = run Analyzer.sentiment(data)
        if sentiment == "negative" {
            negative_found = true
        }
        i = i + 1
        total = total + 1
    }

    string final_report = run Writer.compose(data, "formal")
}
