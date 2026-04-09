agent Researcher {
    tool web_search

    task gather(string topic) -> string data {
        action: web_search(topic)
    }
}

system {
    list topics = ["AI", "DSL"]
    bool found = false

    for topic in topics {
        if topic == "AI" {
            string data = run Researcher.gather(topic)
            found = true
        }
    }
}
