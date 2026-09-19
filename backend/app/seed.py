MOCK_QUESTIONS = [
    {
        "question": "What is the time complexity of binary search?",
        "options": ["O(n)", "O(log n)", "O(n^2)", "O(1)"],
        "correct_answer": 1,
        "explanation": "Binary search halves the search space with each step, resulting in O(log n) time complexity.",
    },
    {
        "question": "Which data structure uses LIFO (Last In, First Out)?",
        "options": ["Queue", "Stack", "Linked List", "Tree"],
        "correct_answer": 1,
        "explanation": "A stack follows LIFO ordering — the last element pushed is the first one popped.",
    },
    {
        "question": "What does DNS stand for?",
        "options": [
            "Data Network Service",
            "Domain Name System",
            "Dynamic Node Selector",
            "Distributed Name Server",
        ],
        "correct_answer": 1,
        "explanation": "DNS (Domain Name System) translates human-readable domain names into IP addresses.",
    },
    {
        "question": "Which protocol is used for secure web browsing?",
        "options": ["HTTP", "FTP", "HTTPS", "SMTP"],
        "correct_answer": 2,
        "explanation": "HTTPS adds TLS encryption to HTTP, ensuring secure communication between browser and server.",
    },
    {
        "question": "What is the purpose of an operating system scheduler?",
        "options": [
            "Manage file storage",
            "Allocate CPU time to processes",
            "Handle network connections",
            "Compile source code",
        ],
        "correct_answer": 1,
        "explanation": "The OS scheduler decides which process gets CPU time and for how long.",
    },
    {
        "question": "What is a deadlock in concurrent systems?",
        "options": [
            "A process that runs forever",
            "A system where no processes can proceed",
            "A memory leak",
            "A stack overflow",
        ],
        "correct_answer": 1,
        "explanation": "Deadlock occurs when two or more processes are blocked forever, each waiting on the other.",
    },
    {
        "question": "Which layer of the OSI model handles encryption?",
        "options": ["Physical", "Data Link", "Presentation", "Session"],
        "correct_answer": 2,
        "explanation": "The Presentation layer is responsible for data translation, compression, and encryption.",
    },
    {
        "question": "What is the primary key in a database?",
        "options": [
            "A key used to encrypt data",
            "A unique identifier for each record",
            "A password for database access",
            "A backup recovery method",
        ],
        "correct_answer": 1,
        "explanation": "A primary key uniquely identifies each row in a database table.",
    },
    {
        "question": "What does 'CI/CD' stand for?",
        "options": [
            "Continuous Integration / Continuous Deployment",
            "Computer Interface / Central Database",
            "Code Inspection / Code Documentation",
            "Compiled Input / Compiled Distribution",
        ],
        "correct_answer": 0,
        "explanation": "CI/CD automates the integration, testing, and deployment of code changes.",
    },
    {
        "question": "Which sorting algorithm has the best average-case time complexity?",
        "options": ["Bubble Sort", "Selection Sort", "Quick Sort", "Insertion Sort"],
        "correct_answer": 2,
        "explanation": "Quick Sort has an average time complexity of O(n log n), making it one of the fastest general-purpose sorting algorithms.",
    },
]

MOCK_FLASHCARDS = [
    {
        "front": "What is a process in an operating system?",
        "back": "A process is a program in execution. It includes the program code, current activity, and allocated resources like memory and file handles.",
    },
    {
        "front": "What is the difference between TCP and UDP?",
        "back": "TCP is connection-oriented and ensures reliable, ordered delivery. UDP is connectionless and faster but does not guarantee delivery or ordering.",
    },
    {
        "front": "What is a hash table?",
        "back": "A hash table is a data structure that maps keys to values using a hash function, providing average O(1) time complexity for lookups, insertions, and deletions.",
    },
    {
        "front": "What is the difference between stack and heap memory?",
        "back": "Stack memory is used for static allocation and follows LIFO. Heap memory is used for dynamic allocation and is managed by the garbage collector or programmer.",
    },
    {
        "front": "What is normalization in databases?",
        "back": "Normalization is the process of organizing a database to reduce redundancy and improve data integrity by splitting large tables into smaller, related ones.",
    },
    {
        "front": "What is an API?",
        "back": "An API (Application Programming Interface) is a set of rules and protocols that allows different software applications to communicate with each other.",
    },
    {
        "front": "What is recursion?",
        "back": "Recursion is a technique where a function calls itself to solve smaller instances of the same problem, using a base case to stop.",
    },
    {
        "front": "What is a thread?",
        "back": "A thread is the smallest unit of execution within a process. Multiple threads within a process share memory and resources.",
    },
]

MOCK_STUDY_NOTES = {
    "title": "Computer Science Fundamentals — Study Notes",
    "summary": (
        "A concise reference covering core computer science topics: "
        "data structures, operating systems, networking, and databases."
    ),
    "sections": [
        {
            "heading": "Data Structures",
            "content": (
                "Data structures organize and store data so it can be used efficiently. "
                "The most common ones are hash tables, stacks, and trees."
            ),
            "bullet_points": [
                "Hash tables map keys to values with O(1) average lookups.",
                "Stacks follow LIFO ordering — the last element pushed is the first popped.",
                "A primary key uniquely identifies each record in a database table.",
            ],
        },
        {
            "heading": "Operating Systems",
            "content": (
                "The operating system (OS) manages hardware resources and provides "
                "an interface for applications. Two key OS concepts are the process "
                "and the scheduler."
            ),
            "bullet_points": [
                "A process is a program in execution, including its code, activity, and resources.",
                "The scheduler allocates CPU time to processes.",
                "Deadlock occurs when processes are blocked forever, each waiting on the other.",
                "A thread is the smallest unit of execution inside a process.",
            ],
        },
        {
            "heading": "Networking & Security",
            "content": (
                "Networking connects computers so they can exchange data. DNS and "
                "HTTPS are two foundational pieces."
            ),
            "bullet_points": [
                "DNS translates human-readable domain names into IP addresses.",
                "HTTPS adds TLS encryption to HTTP for secure web communication.",
                "TCP is reliable and ordered; UDP is faster but does not guarantee delivery.",
            ],
        },
        {
            "heading": "Software Engineering & Databases",
            "content": (
                "Software engineering practices and database design keep systems "
                "reliable, maintainable, and fast."
            ),
            "bullet_points": [
                "CI/CD automates integration, testing, and deployment of code changes.",
                "Normalization reduces redundancy and improves data integrity.",
                "Recursion is a technique where a function calls itself with a base case to stop.",
            ],
        },
    ],
    "key_concepts": [
        {
            "term": "Hash table",
            "definition": "A data structure mapping keys to values with O(1) average lookup, insert, and delete.",
        },
        {
            "term": "Process",
            "definition": "A program in execution, including code, current activity, and allocated resources.",
        },
        {
            "term": "DNS",
            "definition": "Domain Name System — translates domain names into IP addresses.",
        },
        {
            "term": "Normalization",
            "definition": "Organizing a database to reduce redundancy and improve data integrity.",
        },
    ],
}