# PyGDO Oracle

`Oracle` relays questions from one chat channel to subscribed Oracle channels.

* `$oracle.subscribe` subscribes the current channel (staff only).
* `$oracle.ask <question>` creates and broadcasts a question to all subscribed channels.
* `$oracle.answer <id> <answer>` stores an answer and relays it to the asking channel.

Questions, subscriptions, and answers are persisted independently. A question
therefore has a stable ID and can receive more than one answer. Web questions
have no source channel; their persisted answers are shown in the web view.
