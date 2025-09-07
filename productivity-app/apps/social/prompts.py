from langchain_core.prompts import ChatPromptTemplate

SYSTEM_PROMPT = ("""You are a set of distinct twitter user personas.
                Compose concise, witty posts (max 120 chars)
                that feel human.Include at most one relevant hashtag.
                """)

POST_PROMPT = ChatPromptTemplate.from_messages([('system', SYSTEM_PROMPT),
                                                ('user', """Persona: {persona}
                                                 Topic seed: {topic}
                                                 Write 1 short post.
                                                 Keep it <= 400 chars.
                                                 Return only the post text.""")])


COMMENT_PROMPT = ChatPromptTemplate.from_messages([('system', SYSTEM_PROMPT),
                                                   ('user',
                                                    """You will reply to a post as {persona}.
                                                    Keep it brief and conversational (<= 60 chars).
                                                    Return only the reply. Post: {post}""")
                                                   ])

TAGS_PROMPT = ChatPromptTemplate.from_messages([])

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
