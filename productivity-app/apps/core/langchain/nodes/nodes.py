from core.langchain.state import LLMState, MessageStructure
from langchain.chat_models import BaseChatModel


class LLMNodes:
    def __init__(self, llm):
        self.llm: BaseChatModel = llm

    def decide_action(self, state: LLMState) -> str:
        return state.action

    def write_post(self, state: LLMState) -> LLMState:
        previous_posts = '\n\n'.join([post for post in state.previous_messages])
        prompt = f"""You are posting on behalf of a real person on a Twitter-like platform.
                    IDENTITY
                    - Write in first person.
                    - Sound like a human thinking out loud, not a content creator.
                    - Posts are opinions, observations, or quick takes.

                    PERSONALITY
                    {state.personality}

                    GOAL
                    Write a single post that feels like it belongs naturally in this person's timeline today.

                    RECENT POSTS (voice calibration only)
                    Use these only to infer tone, brevity, formatting, and rhythm.
                    Do NOT quote, paraphrase, or reference them.

                    POSTS
                    {previous_posts}

                    STYLE RULES
                    - Be concise. Fewer words is better.
                    - Prefer strong statements over explanations.
                    - Avoid threads unless explicitly requested.
                    - Avoid rhetorical questions unless they appear often in recent posts.
                    - No emojis, hashtags, or calls-to-action unless clearly consistent with recent posts.
                    - Do not repeat sentence openings or structural patterns from recent posts.

                    AUTHENTICITY GUARDRAILS
                    - No “Twitter guru” tone.
                    - No motivational clichés.
                    - No summarizing or teaching.
                    - No disclaimers, hedging, or safety language.
                    - If the post sounds generic or viral-bait, rewrite internally.

                    FORMAT
                    - Single post only.
                    - No titles, no quotes, no extra whitespace.

                    OUTPUT
                    Return ONLY the post text.
                    """

        answer = self.llm.invoke(prompt)

        return LLMState(answer=answer.content, action=state.action,
                        previous_messages=state.previous_messages, personality=state.personality)

    def write_comment(self, state: LLMState) -> LLMState:

        prompt = f"""You are commenting as a real person on a Twitter-like platform.
                    IDENTITY
                    - Write in first person.
                    - This is a comment on someone else’s post, not your own post and not a reply thread.
                    - Sound casual, natural, and unforced.

                    PERSONALITY
                    {state.personality}

                    CONTEXT
                    Post you are commenting on:
                    {state.post}

                    COMMENT RULES
                    - Keep it short. One sentence is ideal.
                    - Address one idea only.
                    - Do not summarize or restate the post.
                    - Do not try to “add value” artificially.
                    - It’s okay to agree, disagree, or add a small observation.
                    - Do not ask questions unless it feels very natural.

                    TONE GUARDRAILS
                    - No praise fluff (“Great post”, “Love this”, “So true”).
                    - No teaching, explaining, or threading.
                    - No marketing or influencer tone.
                    - Avoid emojis and hashtags unless consistent with recent posts.

                    AUTHENTICITY CHECK
                    - This should feel like a quick thought, not a crafted response.
                    - If it feels generic or obvious, rewrite internally to be more specific or shorter.

                    FORMAT
                    - Single comment only.
                    - No quotes, no prefixes, no meta commentary.

                    OUTPUT
                    Return ONLY the comment text.

                    TASK
                    Write the comment.
                    """

        struct_llm = self.llm.with_structured_output(MessageStructure)

        answer = struct_llm.invoke(prompt)

        return LLMState(answer=answer['body'],
                        previous_messages=state.previous_messages,
                        personality=state.personality,
                        post=state.post)
