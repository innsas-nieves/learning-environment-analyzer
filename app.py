import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Learning Environment Analyzer", layout="centered")

# ---- HEADER / BRANDING ---- #
st.title("Learning Environment Analyzer")
st.caption("EPY 690/490 – Introduction to the Learning Sciences, UNLV")

st.write(
    "Use this tool to analyze learning environments using core Learning Sciences "
    "design principles: **scaffolding, ICAP engagement, feedback quality, collaboration, "
    "and metacognitive support**."
)

tabs = st.tabs(
    [
        "Tang et al. (2025) scenarios",
        "Analyze your own environment",
    ]
)

# ---------- TAB 1: PRESET ENVIRONMENTS (TANG ET AL., 2025) ---------- #
with tabs[0]:
    st.subheader("Preset environments from Tang et al. (2025)")

    st.markdown(
        "These three environments come directly from Tang et al. (2025):"
        "\n\n- **Class 1:** Traditional computer-assisted teaching"
        "\n- **Class 2:** Generative AI-assisted teaching, *no* teacher supervision"
        "\n- **Class 3:** Generative AI-assisted teaching *with* teacher supervision"
    )

    environments = {
        "Traditional computer-assisted (Class 1)": {
            "Scaffolding": 3,
            "ICAP engagement": 2,       # mostly Passive/Active
            "Feedback quality": 3,
            "Collaboration": 2,
            "Metacognitive support": 2,
        },
        "GenAI-assisted, no teacher (Class 2)": {
            "Scaffolding": 1,
            "ICAP engagement": 2,
            "Feedback quality": 2,
            "Collaboration": 1,
            "Metacognitive support": 1,
        },
        "GenAI + teacher supervision (Class 3)": {
            "Scaffolding": 4,
            "ICAP engagement": 4,       # more Constructive/Interactive
            "Feedback quality": 4,
            "Collaboration": 2,
            "Metacognitive support": 3,
        },
    }

    choice = st.selectbox("Select environment:", list(environments.keys()))
    scores = environments[choice]

    df = pd.DataFrame(
        {
            "Design principle": list(scores.keys()),
            "Score (1–5)": list(scores.values()),
        }
    )

    st.subheader("Design principle profile")
    fig = px.bar(
        df,
        x="Design principle",
        y="Score (1–5)",
        range_y=[0, 5],
        text="Score (1–5)",
        color="Design principle",
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Interpretation")

    def explain_preset(env_name):
        if "Traditional" in env_name:
            st.markdown(
                """
                **This environment** uses teacher-led computer-assisted instruction.  
                - Engagement is mostly **Passive/Active** (ICAP ≈ 2).  
                - There is some scaffolding and feedback, but it’s not tightly structured.  
                - Metacognition and collaboration are limited.
                
                **Possible improvement:** Add structured prompts that ask students to explain,
                justify, or predict (moving toward **Constructive** engagement).
                """
            )
        elif "no teacher" in env_name:
            st.markdown(
                """
                **This environment** relies on generative AI without teacher supervision.  
                - Scaffolding is almost **absent**.  
                - Engagement stays mostly **Active** (reading/clicking).  
                - Feedback quality and metacognitive support are low.  
                - There is almost no collaboration.
                
                **Risk:** Students may be satisfied but misled or under-challenged.  
                **Possible improvement:** Add teacher or AI-generated metacognitive prompts and
                monitoring to diagnose misconceptions.
                """
            )
        else:
            st.markdown(
                """
                **This environment** combines generative AI with active teacher supervision.  
                - Scaffolding and feedback quality are **high**.  
                - ICAP engagement moves toward **Constructive/Interactive**.  
                - Students show higher engagement and mastery.
                
                **Remaining gaps:**  
                - Collaboration is still limited.  
                - Metacognitive support is not fully explicit.
                
                **Possible improvement:** Design explicit reflection prompts and peer discussion
                around AI outputs.
                """
            )

    explain_preset(choice)

# ---------- TAB 2: USER WIZARD FOR CUSTOM ENVIRONMENTS ---------- #
with tabs[1]:
    st.subheader("Describe and analyze your own learning environment")

    st.markdown(
        "Answer the questions below about a learning environment (a class, project, "
        "or activity). The analyzer will map your answers to design principles and "
        "suggest improvements."
    )

    with st.form("env_form"):
        env_name = st.text_input(
            "Name or short description of your environment (optional):",
            placeholder="e.g., 8th Grade Science Lab, AI-assisted math station, etc.",
        )

        q1 = st.radio(
            "1. How often does a teacher, tutor, or system **adjust support** based on what learners seem to need?",
            [
                "Almost never – support is fixed or absent",
                "Sometimes – some adjustment for struggling learners",
                "Often – support is clearly tailored and responsive",
            ],
        )

        q2 = st.radio(
            "2. What do learners mostly **do** during the activity?",
            [
                "Listen / watch / read (no required action)",
                "Answer questions / complete tasks (short answers, click, copy)",
                "Explain, justify, create, or solve open-ended problems",
                "Discuss, argue, or co-construct ideas with others",
            ],
        )

        q3 = st.radio(
            "3. How is **feedback** usually given?",
            [
                "Mostly right/wrong with little explanation",
                "Some explanation, but not always tied to specific misconceptions",
                "Targeted, explanatory feedback that responds to learner thinking",
            ],
        )

        q4 = st.radio(
            "4. What kind of **collaboration** do learners do?",
            [
                "Mostly individual work",
                "Occasional pair/small group work",
                "Frequent, structured collaboration (roles, shared products, etc.)",
            ],
        )

        q5 = st.radio(
            "5. How much **metacognition** is built into the activity?",
            [
                "Almost none – learners are not asked to reflect or plan",
                "Sometimes – occasional reflection questions or check-ins",
                "Often – learners regularly plan, monitor, and reflect on learning",
            ],
        )

        submitted = st.form_submit_button("Analyze my environment")

    if submitted:
        # Map answers to scores 1–5
        def map_scaffolding(a):
            if "never" in a:
                return 1
            if "Sometimes" in a:
                return 3
            return 5

        def map_icap(a):
            if "Listen" in a:
                return 1
            if "Answer questions" in a:
                return 2
            if "Explain, justify" in a:
                return 4   # Constructive
            return 5       # Interactive

        def map_feedback(a):
            if "right/wrong" in a:
                return 2
            if "Some explanation" in a:
                return 3
            return 5

        def map_collab(a):
            if "individual" in a:
                return 1
            if "Occasional" in a:
                return 3
            return 5

        def map_meta(a):
            if "none" in a:
                return 1
            if "Sometimes" in a:
                return 3
            return 5

        custom_scores = {
            "Scaffolding": map_scaffolding(q1),
            "ICAP engagement": map_icap(q2),
            "Feedback quality": map_feedback(q3),
            "Collaboration": map_collab(q4),
            "Metacognitive support": map_meta(q5),
        }

        # Helper for ICAP label
        def icap_label(score):
            if score <= 1:
                return "Passive (P)"
            if score == 2:
                return "Active (A)"
            if score == 4:
                return "Constructive (C)"
            return "Interactive (I)"

        # Helpers for qualitative labels
        def level_label(score):
            if score <= 2:
                return "low"
            if score == 3:
                return "moderate"
            return "high"

        env_display_name = env_name.strip() if env_name.strip() else "This environment"

        df_custom = pd.DataFrame(
            {
                "Design principle": list(custom_scores.keys()),
                "Score (1–5)": list(custom_scores.values()),
            }
        )

        st.subheader("Your environment’s design profile")

        fig2 = px.bar(
            df_custom,
            x="Design principle",
            y="Score (1–5)",
            range_y=[0, 5],
            text="Score (1–5)",
            color="Design principle",
        )
        fig2.update_traces(textposition="outside")
        fig2.update_layout(showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("Interpretation")

        scaff = custom_scores["Scaffolding"]
        icap = custom_scores["ICAP engagement"]
        feed = custom_scores["Feedback quality"]
        collab = custom_scores["Collaboration"]
        meta = custom_scores["Metacognitive support"]

        # Summary line
        st.markdown(
            f"**Summary:** {env_display_name} appears mostly **{icap_label(icap)}** "
            f"with **{level_label(scaff)} scaffolding** and **{level_label(meta)} metacognitive support**."
        )

        # ICAP explanation text
        if icap <= 1:
            icap_text = (
                "- Engagement is mostly **Passive** (ICAP: P). "
                "Learners receive information but don’t manipulate or generate ideas."
            )
        elif icap == 2:
            icap_text = (
                "- Engagement is mostly **Active** (ICAP: A). "
                "Learners do tasks, but rarely generate new ideas."
            )
        elif icap == 4:
            icap_text = (
                "- Engagement is mostly **Constructive** (ICAP: C). "
                "Learners explain, justify, or create, which supports deeper learning."
            )
        else:
            icap_text = (
                "- Engagement is mostly **Interactive** (ICAP: I). "
                "Learners co-construct ideas through dialogue and collaboration."
            )

        st.markdown(
            f"""
            **Design principle details**

            **Scaffolding:**  
            - Score: {scaff}/5 ({level_label(scaff).capitalize()})  
            {"• Low scaffolding. Consider adding more adaptive teacher or peer support." if scaff <= 2 else ""}
            {"• Moderate scaffolding. You might make support more clearly contingent and plan for fading over time." if scaff == 3 else ""}
            {"• Strong scaffolding. Support seems adaptive; consider planning how it fades to build independence." if scaff >= 4 else ""}

            **ICAP Engagement:**  
            - Score: {icap}/5 ({icap_label(icap)})  
            {icap_text}

            **Feedback quality:**  
            - Score: {feed}/5 ({level_label(feed).capitalize()})  
            {"• Feedback is mostly evaluative. Adding explanations linked to misconceptions could deepen learning." if feed <= 2 else ""}
            {"• Feedback is somewhat explanatory. You could align it more closely with specific errors or strategies." if feed == 3 else ""}
            {"• Feedback appears highly diagnostic and explanatory, which is ideal for learning." if feed >= 4 else ""}

            **Collaboration:**  
            - Score: {collab}/5 ({level_label(collab).capitalize()})  
            {"• Mostly individual. Consider adding structured pair or group activities." if collab <= 2 else ""}
            {"• Some collaboration. You might add roles, shared artifacts, or norms to deepen it." if collab == 3 else ""}
            {"• Collaboration seems well integrated. Check that it supports real co-construction, not just dividing work." if collab >= 4 else ""}

            **Metacognitive support:**  
            - Score: {meta}/5 ({level_label(meta).capitalize()})  
            {"• Little or no metacognition. You could add prompts to plan, monitor, or reflect on learning." if meta <= 2 else ""}
            {"• Some reflection. Making it more regular and tied to strategies could help." if meta == 3 else ""}
            {"• Strong metacognitive support. Learners are regularly guided to reflect and self-regulate." if meta >= 4 else ""}
            """
        )

st.markdown("---")
st.caption(
    "This tool is inspired by Learning Sciences frameworks: Tabak & Reiser (scaffolding), "
    "Chi (ICAP), Winne & Azevedo (metacognition), and Tang et al. (2025) on GenAI-assisted teaching."
)
