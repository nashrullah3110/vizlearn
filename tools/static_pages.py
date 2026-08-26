# -*- coding: utf-8 -*-
"""Copy for the about / contact / privacy / terms pages.

Kept apart from the generator the same way articles.py is, so the wording can
be reviewed and edited without reading any build code.

The privacy policy describes what the site actually loads today: Google
Analytics 4, Google AdSense, Google Fonts, and a handful of localStorage keys.
If a script is added or removed, this file is the place that has to change with
it - `tools/audit.py` cross-checks the analytics and AdSense IDs named here
against the ones the pages really carry.
"""

from lib_pages import CONTACT_EMAIL, GITHUB, KAGGLE, LINKEDIN

GA_ID = "G-ZT6JM33V5J"
ADSENSE_PUB = "ca-pub-7551664560637561"

# Each page: lead paragraph, then (heading, html body) sections.

PAGES = {

# ---------------------------------------------------------------------------
"about.html": {
    "h1": "About VizLearn",
    "lead": "%(modules)d interactive explainers for AI, machine learning, algorithms "
            "and the maths underneath them. Free, and no account required.",
    "description": "VizLearn is a free library of %(modules)d interactive visual explainers for "
                   "AI, machine learning, algorithms and maths. Learn who builds it and "
                   "how the modules are made.",
    "sections": [
        ("Why this exists",
         "<p>Most explanations of these subjects are either a wall of equations or a wall "
         "of prose. Both ask you to simulate the idea in your head and trust that you got "
         "it right. VizLearn is the third option: something you can poke.</p>"
         "<p>Drag a support vector and watch the margin move. Change <em>k</em> and watch "
         "the decision boundary breathe. Step gradient descent one iteration at a time and "
         "watch the line fit. The claim is not that visualisation replaces the maths &mdash; "
         "it is that seeing the mechanism first makes the maths land when you get to it.</p>"),

        ("How a module is built",
         "<p>Every module is a single self-contained page: an interactive visualisation, "
         "the controls that drive it, a live readout of what the algorithm is currently "
         "doing, and a written explanation underneath.</p>"
         "<p>The written part is not filler. Each one covers the mechanism, a worked "
         "example with real numbers, guided experiments you can run in the visualisation "
         "on the same page, and the ways the technique actually fails in practice. Where a "
         "page states a number, that number comes from the same computation the "
         "visualisation is running.</p>"),

        ("How the tracks fit together",
         "<p>The %(modules)d modules are grouped into %(tracks)d tracks, and within a track they are "
         "ordered so that each module only leans on ideas introduced before it. Every page "
         "links to the previous and next step, so a track can be read straight through.</p>"
         "<p>If you are starting from nothing, the <a href=\"index.html#learning-path\">"
         "Learning Path</a> is a curated 25-module route that crosses tracks &mdash; the "
         "maths everything assumes, then the machine learning core, then enough of each "
         "specialism to choose one.</p>"),

        ("Who makes it",
         "<p>VizLearn is built and maintained by Ashish Jangra. You can find more of the "
         "work on <a href=\"%s\" target=\"_blank\" rel=\"noopener noreferrer\">GitHub</a>, "
         "<a href=\"%s\" target=\"_blank\" rel=\"noopener noreferrer\">LinkedIn</a> and "
         "<a href=\"%s\" target=\"_blank\" rel=\"noopener noreferrer\">Kaggle</a>.</p>"
         "<p>Corrections are genuinely welcome. If a module states something wrong, or an "
         "animation misrepresents what the algorithm does, please "
         "<a href=\"contact.html\">get in touch</a> &mdash; that is the fastest way to make "
         "the site better.</p>" % (GITHUB, LINKEDIN, KAGGLE)),

        ("How it is funded",
         "<p>VizLearn is free to use and does not require an account. It is supported by "
         "display advertising, which is what pays for the domain and the time that goes "
         "into new modules. Ads never sit inside a visualisation and never gate a page.</p>"
         "<p>Advertising means third-party cookies, so the "
         "<a href=\"privacy.html\">Privacy Policy</a> sets out exactly what is collected "
         "and how to opt out.</p>"),

        ("The technology, briefly",
         "<p>The site is static HTML, served straight from a repository with no framework "
         "and no backend. Every visualisation is hand-written SVG driven by plain "
         "JavaScript, which is why the pages load quickly and keep working offline once "
         "they are open.</p>"
         "<p>Your progress, your theme and your quiz answers live in your own browser's "
         "local storage. There is no user database, because there are no users &mdash; "
         "nothing about what you read is sent anywhere.</p>"),
    ],
},

# ---------------------------------------------------------------------------
"contact.html": {
    "h1": "Contact",
    "lead": "Corrections, questions, requests for a module that does not exist yet.",
    "description": "Get in touch with VizLearn about a correction, a question, a "
                   "suggested module, or a licensing or advertising enquiry.",
    "sections": [
        ("Email",
         "<p>The most reliable way to reach me is email:</p>"
         "<p class=\"vz-contact-primary\"><a href=\"mailto:%s\">%s</a></p>"
         "<p>I read everything. I do not always reply quickly, but corrections get "
         "priority over everything else.</p>" % (CONTACT_EMAIL, CONTACT_EMAIL)),

        ("Found something wrong?",
         "<p>Please say so. When you write in, it helps enormously if you include:</p>"
         "<ul class=\"vz-list\">"
         "<li>the page &mdash; the full URL, or just the module name</li>"
         "<li>what it says, and what you believe it should say</li>"
         "<li>if it is the visualisation rather than the text, the control settings that "
         "produce the problem, and what browser you are on</li>"
         "</ul>"
         "<p>Factual errors in the written explanations, and animations that misrepresent "
         "the algorithm, are the two things I most want to hear about.</p>"),

        ("What happens to a correction",
         "<p>Every page on this site is generated from source rather than edited by hand, "
         "so a fix is never a patch to one file. A reported error gets reproduced first, "
         "then corrected at the point it comes from &mdash; the written explanation, the "
         "code that draws the visualisation, or the numbers the two share &mdash; and the "
         "whole site is rebuilt from there.</p>"
         "<p>That is slower than editing a page in place, but it means the same mistake "
         "cannot survive somewhere else. When a module states a number, that number is "
         "computed by the same code the visualisation runs, so a correction to one is "
         "automatically a correction to the other.</p>"
         "<p>Once a fix ships, the module's updated date changes and the change is listed "
         "on <a href=\"whats-new/\">What's New</a>, so you can confirm it landed without "
         "having to take my word for it.</p>"),

        ("How long a reply takes",
         "<p>This is a one-person site with no support desk behind it, so there is no "
         "service-level promise to make. In practice: a clear factual correction usually "
         "gets acknowledged within a few days and fixed in the same week, because it is "
         "the highest-value message I receive. A module request, a licensing question or "
         "anything that needs a considered answer can take longer.</p>"
         "<p>If a fortnight goes by with nothing, the message went astray rather than "
         "being ignored &mdash; send it again.</p>"),

        ("Requesting a module",
         "<p>If there is a topic you keep failing to find a good explanation of, send it "
         "over. Requests that name the specific thing that is confusing (\"why does padding "
         "change the output size\") are far more useful than a broad subject, because the "
         "confusion is what a module is built around.</p>"),

        ("What this address is not for",
         "<p>I cannot debug your code, complete an assignment, or work through a problem "
         "set for you. If a module left you unable to do something the module claims to "
         "teach, that is worth writing in about, because it means the explanation is not "
         "doing its job &mdash; but frame it that way rather than as a question to be "
         "answered.</p>"
         "<p>For running code, the five labs on this site &mdash; "
         "<a href=\"python-lab/\">Python</a>, <a href=\"pydantic-lab/\">Pydantic</a>, "
         "<a href=\"sql-lab/\">SQL</a>, "
         "<a href=\"js-lab/\">JavaScript</a> and <a href=\"html-lab/\">HTML</a> "
         "&mdash; run entirely in your browser and will usually tell you more, faster, "
         "than an email will.</p>"),

        ("Using VizLearn in teaching",
         "<p>You are welcome to link to any module from a course page, a reading list or a "
         "lecture, and to use it live in a classroom. No permission needed. If you want to "
         "reproduce a visualisation or the written text somewhere else, check the "
         "<a href=\"terms.html\">Terms of Use</a> first, then email me.</p>"),

        ("Advertising, licensing and press",
         "<p>For anything commercial &mdash; sponsorship, licensing the visualisations, or "
         "a press enquiry &mdash; use the same address and put the subject in the first "
         "line so it does not get lost behind the corrections.</p>"),

        ("Elsewhere",
         "<p><a href=\"%s\" target=\"_blank\" rel=\"noopener noreferrer\">GitHub</a> "
         "&middot; <a href=\"%s\" target=\"_blank\" rel=\"noopener noreferrer\">LinkedIn</a> "
         "&middot; <a href=\"%s\" target=\"_blank\" rel=\"noopener noreferrer\">Kaggle</a></p>"
         % (GITHUB, LINKEDIN, KAGGLE)),
    ],
},

# ---------------------------------------------------------------------------
"privacy.html": {
    "h1": "Privacy Policy",
    "lead": "What VizLearn collects, who else receives it, and how to switch "
            "the tracking off.",
    "description": "VizLearn's privacy policy: the analytics and advertising cookies the "
                   "site sets, the data stored in your browser, and how to opt out.",
    "sections": [
        ("The short version",
         "<p>VizLearn has no accounts, no sign-up and no server of its own. It never asks "
         "for your name, your email or any other personal detail, and it stores nothing "
         "about you on any machine it controls.</p>"
         "<p>It does load three Google services &mdash; Analytics, AdSense and Fonts &mdash; "
         "and those do set cookies and do receive your IP address. Everything below is the "
         "detail of that.</p>"),

        ("Information you give us",
         "<p>None. There is no registration form, no newsletter signup, no comment box and "
         "no upload. If you email me, I have your email address and whatever you put in the "
         "message, and I use it only to reply to you.</p>"),

        ("Information collected automatically",
         "<p>Like almost every website, the third-party services below receive standard "
         "request information when a page loads: your IP address, your browser and "
         "operating system, the page you are on, the page that referred you, and the date "
         "and time.</p>"),

        ("Analytics",
         "<p>VizLearn uses <strong>Google Analytics 4</strong> (measurement ID "
         "<span class=\"mono-font\">%s</span>) to count visits and see which modules people "
         "actually read. It sets cookies to tell one visit from the next, and it reports to "
         "me only in aggregate &mdash; page counts, countries, device types. I cannot "
         "identify an individual reader from it, and I do not try to.</p>"
         "<p>Google's own description of the data it processes is in the "
         "<a href=\"https://policies.google.com/privacy\" target=\"_blank\" "
         "rel=\"noopener noreferrer\">Google Privacy Policy</a> and in "
         "<a href=\"https://business.safety.google/privacy/\" target=\"_blank\" "
         "rel=\"noopener noreferrer\">How Google uses data from sites that use its "
         "services</a>.</p>" % GA_ID),

        ("Advertising",
         "<p>VizLearn shows ads through <strong>Google AdSense</strong> (publisher ID "
         "<span class=\"mono-font\">%s</span>). To do that, Google and its partners set "
         "cookies in your browser.</p>"
         "<ul class=\"vz-list\">"
         "<li>Google uses cookies, including the <span class=\"mono-font\">DoubleClick</span> "
         "cookie, to serve ads based on your prior visits to this and other websites.</li>"
         "<li>Third-party vendors and ad networks may also serve ads on this site and set "
         "their own cookies. VizLearn does not control those cookies and cannot read "
         "them.</li>"
         "<li>Personalised advertising can be switched off entirely at "
         "<a href=\"https://www.google.com/settings/ads\" target=\"_blank\" "
         "rel=\"noopener noreferrer\">Google Ads Settings</a>. Ads still appear; they stop "
         "being tailored to you.</li>"
         "<li>To opt out of a wider set of vendors at once, use "
         "<a href=\"https://optout.aboutads.info/\" target=\"_blank\" "
         "rel=\"noopener noreferrer\">aboutads.info</a> or "
         "<a href=\"https://optout.networkadvertising.org/\" target=\"_blank\" "
         "rel=\"noopener noreferrer\">the NAI opt-out page</a>.</li>"
         "</ul>"
         "<p>The ads.txt file at "
         "<a href=\"ads.txt\">vizlearn.in/ads.txt</a> declares which sellers are authorised "
         "to sell inventory on this domain.</p>" % ADSENSE_PUB),

        ("Fonts",
         "<p>Typefaces are loaded from <strong>Google Fonts</strong>. Making that request "
         "reveals your IP address to Google. Google states that Fonts requests do not set "
         "cookies and are not used for advertising.</p>"),

        ("Data stored in your browser",
         "<p>VizLearn keeps a small amount of state in your browser's "
         "<span class=\"mono-font\">localStorage</span>. This never leaves your device and "
         "is not readable by me or by any third party:</p>"
         "<ul class=\"vz-list\">"
         "<li><span class=\"mono-font\">theme</span> &mdash; whether you chose light or "
         "dark mode.</li>"
         "<li><span class=\"mono-font\">vizlearn_progress</span> &mdash; which modules you "
         "have opened and when, so the site can draw checkmarks and offer to resume.</li>"
         "<li><span class=\"mono-font\">vizlearn_checks</span> &mdash; your answers to the "
         "end-of-module questions, so a page remembers what you already got right.</li>"
         "</ul>"
         "<p>Clearing your browser's site data for vizlearn.in erases all of it and resets "
         "the site to a first visit. Nothing is backed up, so this cannot be undone.</p>"),

        ("Hosting and logs",
         "<p>The site is static and is served by a third-party static host, which keeps "
         "standard server access logs for security and abuse prevention. I do not have "
         "access to raw logs that identify individual visitors.</p>"),

        ("Children",
         "<p>VizLearn is aimed at learners aged roughly 16 and up and is not directed at "
         "children under 13. I do not knowingly collect any information from children under "
         "13. If you believe a child has provided information by emailing me, write in and "
         "I will delete it.</p>"),

        ("Your rights",
         "<p>Depending on where you live, you may have rights over personal data held about "
         "you &mdash; to see it, correct it, delete it, or object to its processing. This "
         "matters mostly for the data <em>Google</em> holds, since VizLearn holds none.</p>"
         "<ul class=\"vz-list\">"
         "<li><strong>If you are in the EEA or UK (GDPR):</strong> advertising and analytics "
         "cookies are set on the basis of consent, which you can withdraw at any time using "
         "the links above or by blocking cookies in your browser.</li>"
         "<li><strong>If you are in California (CCPA/CPRA):</strong> VizLearn does not sell "
         "or share personal information for money. Interest-based advertising may count as "
         "\"sharing\" under the CPRA; the Google Ads Settings link above turns it off.</li>"
         "</ul>"
         "<p>For anything held by Google, Google is the controller and its own privacy tools "
         "are the route to act on it. For the email you sent me, "
         "<a href=\"contact.html\">write in</a> and I will delete it on request.</p>"),

        ("Controlling cookies yourself",
         "<p>Every major browser can block or delete cookies, and most offer a setting that "
         "blocks third-party cookies specifically &mdash; which stops the advertising and "
         "analytics cookies described here while leaving the site fully usable. Browser "
         "extensions that block trackers have the same effect. Nothing on VizLearn requires "
         "a cookie to work.</p>"),

        ("External links",
         "<p>Modules link out to papers, documentation and other resources. Once you follow "
         "one of those links you are on someone else's site, under their privacy policy, "
         "not this one.</p>"),

        ("Changes to this policy",
         "<p>If the scripts the site loads change, this page changes with them, and the "
         "\"last updated\" date at the top moves. Material changes will be obvious from that "
         "date &mdash; there is no mailing list to notify.</p>"),

        ("Contact",
         "<p>Questions about this policy, or a request about your data, go to "
         "<a href=\"mailto:%s\">%s</a>. See the <a href=\"contact.html\">contact page</a> "
         "for everything else.</p>" % (CONTACT_EMAIL, CONTACT_EMAIL)),
    ],
},

# ---------------------------------------------------------------------------
"terms.html": {
    "h1": "Terms of Use",
    "lead": "What you may do with the material on VizLearn, and the limits on "
            "what it promises.",
    "description": "Terms of use for VizLearn: permitted use of the interactive modules "
                   "and written explanations, accuracy, and limitation of liability.",
    "sections": [
        ("Using the site",
         "<p>VizLearn is free to use for learning and for teaching. You do not need an "
         "account and you do not need to ask permission to read, link to, bookmark or use "
         "any module in a classroom.</p>"
         "<p>By using the site you accept these terms. If you do not, please stop using "
         "it.</p>"),

        ("What you may do without asking",
         "<ul class=\"vz-list\">"
         "<li>Link to any page, from anywhere.</li>"
         "<li>Use modules live in a lecture, workshop, tutorial or study group.</li>"
         "<li>Put a module on a reading list or in course materials, as a link.</li>"
         "<li>Take screenshots for a talk, a blog post or a paper, with attribution to "
         "vizlearn.in.</li>"
         "<li>Copy a cheat sheet for your own notes &mdash; there is a button for it.</li>"
         "</ul>"),

        ("What needs permission",
         "<p>The written explanations and the visualisations on this site are original work "
         "and remain copyright of their author. Please ask before you republish a module's "
         "text elsewhere, mirror pages on another domain, embed a visualisation in a "
         "commercial product or paid course, or use the material to train or fine-tune a "
         "model for redistribution.</p>"
         "<p>The site's source code is published separately under the MIT licence; that "
         "licence covers the code, not the written explanations.</p>"),

        ("Accuracy",
         "<p>Every module is written to be correct and the visualisations run the real "
         "computation rather than a canned animation. Even so, the explanations simplify: "
         "they are teaching material, not specifications, and a visualisation is a model of "
         "an algorithm rather than a reference implementation.</p>"
         "<p>Do not rely on VizLearn as the sole basis for a production system, an academic "
         "submission, a medical or financial decision, or anything else with real "
         "consequences. Check the primary sources. And if you find an error, "
         "<a href=\"contact.html\">tell me</a>.</p>"),

        ("Availability",
         "<p>The site is provided as-is and as-available. Modules may be edited, reordered "
         "or removed, URLs may change, and there is no guarantee of uptime. Your saved "
         "progress lives only in your own browser, so it disappears if you clear site data "
         "&mdash; there is no backup and no way to recover it.</p>"),

        ("Advertising and external links",
         "<p>Pages carry third-party advertising. Ads are selected by the ad network, not "
         "by me, and an ad appearing on VizLearn is not an endorsement of what it "
         "advertises. The same goes for outbound links: they are there because they are "
         "useful, and I am not responsible for what those sites do or say.</p>"),

        ("Limitation of liability",
         "<p>To the fullest extent the law allows, VizLearn and its author are not liable "
         "for any loss or damage arising out of your use of the site, including any loss of "
         "saved progress, and give no warranties of any kind, express or implied, including "
         "fitness for a particular purpose.</p>"),

        ("Changes",
         "<p>These terms may change. The date at the top of the page shows when they last "
         "did, and continuing to use the site after that is acceptance of the revised "
         "terms.</p>"),

        ("Contact",
         "<p>Questions about these terms, or a permission request, go to "
         "<a href=\"mailto:%s\">%s</a>.</p>" % (CONTACT_EMAIL, CONTACT_EMAIL)),
    ],
},

}
