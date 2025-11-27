import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Learning Environment Analyzer", layout="centered")

st.title("Learning Environment Analyzer")
st.write("Based on Tang et al. (2025) and Learning Sciences design principles.")

st.markdown("Choose a learning environment to see how it scores on key design principles:")

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

def explain(env_name, scores_dict):
    if "Traditional" in env_name:
        st.markdown("""
        **This environment** uses teacher-led computer-assisted instruction.  
        - Engagement is mostly **Passive/Active** (ICAP ≈ 2).  
        - There is some scaffolding and feedback, but it’s not tightly structured.  
        - Metacognition and collaboration are limited.
        
        **Possible improvement:** Add structured prompts that ask students to explain,
        justify, or predict (moving toward **Constructive** engagement).
        """)
    elif "no teacher" in env_name:
        st.markdown("""
        **This environment** relies on generative AI without teacher supervision.  
        - Scaffolding is almost **absent**.  
        - Engagement stays mostly **Active** (reading/clicking).  
        - Feedback quality and metacognitive support are low.  
        - There is almost no collaboration.
        
        **Risk:** Students may be satisfied but misled or under-challenged.  
        **Possible improvement:** Add teacher or AI-generated metacognitive prompts and
        monitoring to diagnose misconceptions.
        """)
    else:
        st.markdown("""
        **This environment** combines generative AI with active teacher supervision.  
        - Scaffolding and feedback quality are **high**.  
        - ICAP engagement moves toward **Constructive/Interactive**.  
        - Students show higher engagement and mastery.
        
        **Remaining gaps:**  
        - Collaboration is still limited.  
        - Metacognitive support is not fully explicit.
        
        **Possible improvement:** Design explicit reflection prompts and peer discussion
        around AI outputs.
        """)

explain(choice, scores)

st.markdown("---")
st.caption(
    "Design principles drawn from Tabak & Reiser (scaffolding), Chi (ICAP), "
    "Winne & Azevedo (metacognition), and Tang et al. (2025)."
)
