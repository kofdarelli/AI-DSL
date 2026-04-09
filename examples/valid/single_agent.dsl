agent Writer {
    tool llm

    task draft(string topic, int count) -> string document {
        action: llm(topic, count)
    }
}

system {
    string topic = "compiler design"
    int count = 2
    string document = run Writer.draft(topic, count)
}
