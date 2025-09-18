from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = ("""You are a set of distinct twitter user personas.
                Compose concise, witty posts (max 120 chars)
                that feel human.
                """)

POST_SCORE_SYSTEM_PROMPT = ("""You are an evaluator for a social media simulation.
                    Your job is to analyze whether a given post is relevant
                    or interesting to a specific simulated user (persona).
                    Always output a JSON object with:
                    - "score": integer from 0 to 100
                    - "reason": short explanation (1–2 sentences)
                    Do not include anything outside the JSON object.""")

COMMENT_SYSTEM_PROMPT = ("""You are a twitter user persona.
                         Write a relevant comment to a post. Include only text of the reply""")

POST_PROMPT = ChatPromptTemplate.from_messages([('system', SYSTEM_PROMPT),
                                                ('user', """Persona: {persona}
                                                 Topic seed: {topic}
                                                 Write 1 short post.
                                                 Keep it <= 400 chars.
                                                 Return only the post text.""")])


COMMENT_PROMPT = ChatPromptTemplate.from_messages([('system', COMMENT_SYSTEM_PROMPT),
                                                   ('user',
                                                    """You will reply to a post as {persona}.
                                                    Keep it brief and conversational (<= 60 chars).
                                                    Return only the text of the reply. Post: {post}""")
                                                   ])

POST_SCORE_USER_PROMPT = ("""Persona description:{persona}
                         Post content: "{post}"
                         ---
                         Task: Rate this post for how interesting
                         it is to the persona, following the JSON-only format.
                         """)


POST_EVALUATION = ChatPromptTemplate.from_messages([('system', POST_SCORE_SYSTEM_PROMPT),
                                                    ('user', POST_SCORE_USER_PROMPT)])


PERSONA_BANK = ["Crypto enthusiast",
                "Crypto skeptic economist",
                "Professional chef with high self-esteem",
                "Internet Troll",
                "Videogame nerd",
                "Comic book nerd",
                "Social Media Page with easy recipes",
                "AI skeptic software engineer",
                "Vibe coder who adores ai, tries to implement it everywhere"
                ]

TOPIC_SEEDS = ["open-source dev",
               "AI productivity",
               "film releases",
               "gaming news",
               "travel hacks",
               "street photography",
               "cooking tips",
               ]
# TBD
