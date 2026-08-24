# PyGDO Oracle

`Oracle` relays questions from one chat channel to subscribed Oracle channels.
Question creation is deliberately decoupled from delivery: the caller persists
the question, emits an IPC event containing its ID, and only Dog fans it out.
This lets web and chat create questions through the same safe path.

* `$oracle.subscribe` subscribes the current channel (voice permission).
* `$oracle.ask <question>` creates and broadcasts a question to all subscribed channels.
* `$oracle.answer <id> <answer>` stores an answer and relays it to the asking channel.

Questions, subscriptions, and answers are persisted independently. A question
therefore has a stable ID and can receive more than one answer. Web questions
have no source channel; their persisted answers are shown in the web view.
The web ask flow redirects to the single-question answer view through an
opaque HMAC access token. That view refreshes after `refresh_timeout`
(seven seconds by default).

Subscribing a channel is idempotent: calling `$oracle.subscribe` again keeps
its existing subscription rather than creating a duplicate.
