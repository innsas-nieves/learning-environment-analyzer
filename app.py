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
        # --------- scoring helpers --------- #
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

        def capitalize_first(s: str) -> str:
            return s[0].upper() + s[1:] if s else s

        env_display_name = env_name.strip() if env_name.strip() else "This environment"

        df_custom = pd.DataFrame(
            {
                "Design principle": list(custom_scores.keys()),
                "Score (1–5)": list(custom_scores.values()),
            }
        )

        st.subheader("Your environment’s design profile")

        scaff = custom_scores["Scaffolding"]
        icap = custom_scores["ICAP engagement"]
        feed = custom_scores["Feedback quality"]
        collab = custom_scores["Collaboration"]
        meta = custom_scores["Metacognitive support"]

        # -------- Summary line ABOVE chart -------- #
        summary_line = (
            f"**Summary:** {env_display_name} appears mostly **{icap_label(icap)}** "
            f"with **{level_label(scaff)} scaffolding** and "
            f"**{level_label(meta)} metacognitive support**."
        )
        st.markdown(summary_line)

        # -------- Impact on learning -------- #
        impact_parts = []

        # ICAP impact
        if icap <= 1:
            impact_parts.append(
                "students mainly receive information passively, so knowledge may remain inert and hard to transfer."
            )
        elif icap == 2:
            impact_parts.append(
                "students are active but not generative, so they may complete tasks without fully understanding underlying concepts."
            )
        elif icap == 4:
            impact_parts.append(
                "students engage constructively, which usually supports deeper understanding and integration of ideas."
            )
        else:
            impact_parts.append(
                "students engage interactively, which often supports co-construction of ideas and deeper learning."
            )

        # Scaffolding impact
        if scaff <= 2:
            impact_parts.append(
                "Because scaffolding is low, struggling learners may not get enough adaptive support and can stay confused or fall behind."
            )
        elif scaff == 3:
            impact_parts.append(
                "With moderate scaffolding, some learners receive help, but support might not always be contingent or faded over time."
            )
        else:
            impact_parts.append(
                "High scaffolding can help keep learners in their zone of proximal development, as long as support is gradually faded to build independence."
            )

        # Metacognition impact
        if meta <= 2:
            impact_parts.append(
                "Low metacognitive support means students have fewer opportunities to plan, monitor, and reflect, which can limit long-term self-regulation."
            )
        elif meta == 3:
            impact_parts.append(
                "Some metacognitive support is present, but making reflection more regular and strategy-focused could strengthen durable learning."
            )
        else:
            impact_parts.append(
                "Strong metacognitive support can help learners take more ownership of their learning and transfer strategies to new contexts."
            )

        impact_text = " ".join(impact_parts)

        st.markdown(
            f"**Impact on learning:** {capitalize_first(impact_text)}"
        )

        st.markdown("---")

        # -------- Chart -------- #
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

        # -------- Interpretation -------- #
        st.subheader("Interpretation")
        st.markdown("### Design principle details")

        # ICAP explanation text for reuse
        if icap <= 1:
            icap_text = (
                "Engagement is mostly **Passive** (ICAP: P). "
                "Learners receive information but don’t manipulate or generate ideas."
            )
        elif icap == 2:
            icap_text = (
                "Engagement is mostly **Active** (ICAP: A). "
                "Learners do tasks, but rarely generate new ideas."
            )
        elif icap == 4:
            icap_text = (
                "Engagement is mostly **Constructive** (ICAP: C). "
                "Learners explain, justify, or create, which supports deeper learning."
            )
        else:
            icap_text = (
                "Engagement is mostly **Interactive** (ICAP: I). "
                "Learners co-construct ideas through dialogue and collaboration."
            )

        # Scaffolding
        st.markdown(
            f"**Scaffolding**  \n"
            f"- Score: {scaff}/5 ({level_label(scaff).capitalize()})  \n"
            f"{'• Low scaffolding. Consider adding more adaptive teacher or peer support.' if scaff <= 2 else ''}"
            f"{'• Moderate scaffolding. You might make support more clearly contingent and plan for fading over time.' if scaff == 3 else ''}"
            f"{'• Strong scaffolding. Support seems adaptive; consider planning how it fades to build independence.' if scaff >= 4 else ''}"
        )

        st.markdown("")

        # ICAP
        st.markdown(
            f"**ICAP engagement**  \n"
            f"- Score: {icap}/5 ({icap_label(icap)})  \n"
            f"• {icap_text}"
        )

        st.markdown("")

        # Feedback
        st.markdown(
            f"**Feedback quality**  \n"
            f"- Score: {feed}/5 ({level_label(feed).capitalize()})  \n"
            f"{'• Feedback is mostly evaluative. Adding explanations linked to misconceptions could deepen learning.' if feed <= 2 else ''}"
            f"{'• Feedback is somewhat explanatory. You could align it more closely with specific errors or strategies.' if feed == 3 else ''}"
            f"{'• Feedback appears highly diagnostic and explanatory, which is ideal for learning.' if feed >= 4 else ''}"
        )

        st.markdown("")

        # Collaboration
        st.markdown(
            f"**Collaboration**  \n"
            f"- Score: {collab}/5 ({level_label(collab).capitalize()})  \n"
            f"{'• Mostly individual. Consider adding structured pair or group activities.' if collab <= 2 else ''}"
            f"{'• Some collaboration. You might add roles, shared artifacts, or norms to deepen it.' if collab == 3 else ''}"
            f"{'• Collaboration seems well integrated. Check that it supports real co-construction, not just dividing work.' if collab >= 4 else ''}"
        )

        st.markdown("")

        # Metacognition
        st.markdown(
            f"**Metacognitive support**  \n"
            f"- Score: {meta}/5 ({level_label(meta).capitalize()})  \n"
            f"{'• Little or no metacognition. You could add prompts to plan, monitor, or reflect on learning.' if meta <= 2 else ''}"
            f"{'• Some reflection. Making it more regular and tied to strategies could help.' if meta == 3 else ''}"
            f"{'• Strong metacognitive support. Learners are regularly guided to reflect and self-regulate.' if meta >= 4 else ''}"
        )

        # For download text, reconstruct a compact interpretation string
        interpretation_text = (
            "Scaffolding:\n"
            f"- Score: {scaff}/5 ({level_label(scaff)})\n"
            "ICAP engagement:\n"
            f"- Score: {icap}/5 ({icap_label(icap)})\n"
            f"- {icap_text}\n"
            "Feedback quality:\n"
            f"- Score: {feed}/5 ({level_label(feed)})\n"
            "Collaboration:\n"
            f"- Score: {collab}/5 ({level_label(collab)})\n"
            "Metacognitive support:\n"
            f"- Score: {meta}/5 ({level_label(meta)})\n"
        )

        # -------- Design improvement summary -------- #
        st.markdown("---")
        st.subheader("Design improvement summary")

        improvements = []

        if scaff <= 2:
            improvements.append(
                "Increase **adaptive scaffolding** (teacher, peers, or tools) that responds to learner difficulty."
            )
        if icap <= 2:
            improvements.append(
                "Redesign tasks so learners must **explain, justify, or create**, moving beyond simple completion."
            )
        if collab <= 2:
            improvements.append(
                "Add **structured collaboration** (pairs/groups with roles and shared artifacts)."
            )
        if meta <= 2:
            improvements.append(
                "Embed regular **metacognitive prompts** (plan, monitor, reflect on strategies and understanding)."
            )
        if feed <= 2:
            improvements.append(
                "Shift feedback from right/wrong toward **diagnostic explanations** linked to misconceptions."
            )

        if not improvements:
            improvements.append(
                "This environment already reflects many strong design principles. Future work could focus on fine-tuning "
                "task design and alignment across scaffolding, collaboration, and metacognition."
            )

        improvement_paragraph = " ".join(improvements)
        st.write(improvement_paragraph)

        # -------- Download button -------- #
        impact_for_download = capitalize_first(impact_text)

        download_text = (
            f"Learning Environment Analysis – {env_display_name}\n\n"
            f"Scaffolding: {scaff}/5 ({level_label(scaff)})\n"
            f"ICAP engagement: {icap}/5 ({icap_label(icap)})\n"
            f"Feedback quality: {feed}/5 ({level_label(feed)})\n"
            f"Collaboration: {collab}/5 ({level_label(collab)})\n"
            f"Metacognitive support: {meta}/5 ({level_label(meta)})\n\n"
            f"Summary:\n{summary_line}\n\n"
            f"Impact on learning:\n{impact_for_download}\n\n"
            "Interpretation:\n"
            f"{interpretation_text}\n\n"
            "Design improvement summary:\n"
            f"{improvement_paragraph}\n"
        )

        st.download_button(
            label="Download this analysis",
            data=download_text,
            file_name="learning_environment_analysis.txt",
            mime="text/plain",
        )

st.markdown("---")
st.caption(
    "This tool is inspired by Learning Sciences frameworks: Tabak & Reiser (scaffolding), "
    "Chi (ICAP), Winne & Azevedo (metacognition), and Tang et al. (2025) on GenAI-assisted teaching."
)

with st.expander("References (APA)"):
    st.markdown(
        """
Chi, M. T. H. (2018). ICAP: How students engage to learn. *Proceedings of the Annual Meeting of the Cognitive Science Society, 40*.

Chi, M. T. H., & Wylie, R. (2014). The ICAP framework: Linking cognitive engagement to active learning outcomes. *Educational Psychologist, 49*(4), 219–243. https://doi.org/10.1080/00461520.2014.965823

Tabak, I., & Reiser, B. J. (2022). Scaffolding. In R. K. Sawyer (Ed.), *The Cambridge Handbook of the Learning Sciences* (3rd ed., pp. 53–71). Cambridge University Press. https://doi.org/10.1017/9781108888295.005

Tang, Q., Deng, W., Huang, Y., Wang, S., & Zhang, H. (2025). Can generative artificial intelligence be a good teaching assistant?—An empirical analysis based on generative AI-assisted teaching. *Journal of Computer Assisted Learning, 41*(3), e70027. https://doi.org/10.1111/jcal.70027

Winne, P. H., & Azevedo, R. (2022). Metacognition and self-regulated learning. In R. K. Sawyer (Ed.), *The Cambridge Handbook of the Learning Sciences* (3rd ed., pp. 93–113). Cambridge University Press. https://doi.org/10.1017/9781108888295.007
        """
    )
