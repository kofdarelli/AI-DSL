agent Researcher {
    tool web_search

    task gather(string topic) -> string data {
        action: web_search(topic)
    }
}

system {
    bool valid = true
