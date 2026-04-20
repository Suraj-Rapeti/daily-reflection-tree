graph TD
    START["START<br/>Good evening. Before the day..."]
    START --> A1_OPEN["A1_OPEN<br/>If you had to pick one word..."]
    
    A1_OPEN --> A1_D1["A1_D1<br/>Decision"]
    
    A1_D1 -->|Productive, Mixed| A1_Q_AGENCY_HIGH["A1_Q_AGENCY_HIGH<br/>When something went well..."]
    A1_D1 -->|Tough, Frustrating| A1_Q_AGENCY_LOW["A1_Q_AGENCY_LOW<br/>When things got difficult..."]
    
    A1_Q_AGENCY_HIGH --> A1_D2_HIGH["A1_D2_HIGH<br/>Decision"]
    A1_Q_AGENCY_LOW --> A1_D2_LOW["A1_D2_LOW<br/>Decision"]
    
    A1_D2_HIGH -->|Internal| A1_Q_SETBACK_INT["A1_Q_SETBACK_INT<br/>Did you feel like you had a choice?"]
    A1_D2_HIGH -->|External| A1_Q_SETBACK_EXT["A1_Q_SETBACK_EXT<br/>Was there anything you could influence?"]
    
    A1_D2_LOW -->|Internal| A1_Q_SETBACK_INT
    A1_D2_LOW -->|External| A1_Q_SETBACK_EXT
    
    A1_Q_SETBACK_INT --> A1_D3["A1_D3<br/>Decision"]
    A1_Q_SETBACK_EXT --> A1_D3
    
    A1_D3 -->|Strong Internal| A1_R_STRONG_INT["A1_R_STRONG_INT<br/>Reflection: Agency"]
    A1_D3 -->|Soft Internal| A1_R_SOFT_INT["A1_R_SOFT_INT<br/>Reflection: Partial Agency"]
    A1_D3 -->|External| A1_R_EXT["A1_R_EXT<br/>Reflection: External Focus"]
    
    A1_R_STRONG_INT --> BRIDGE_1_2["BRIDGE_1_2<br/>Bridge to Axis 2"]
    A1_R_SOFT_INT --> BRIDGE_1_2
    A1_R_EXT --> BRIDGE_1_2
    
    BRIDGE_1_2 --> A2_OPEN["A2_OPEN<br/>Most significant interaction?"]
    
    A2_OPEN --> A2_D1["A2_D1<br/>Decision"]
    
    A2_D1 -->|Contribution| A2_Q_CONTRIB["A2_Q_CONTRIB<br/>What motivated that action?"]
    A2_D1 -->|Entitlement| A2_Q_ENTITLEMENT["A2_Q_ENTITLEMENT<br/>What were you comparing against?"]
    
    A2_Q_CONTRIB --> A2_Q_EXTRA["A2_Q_EXTRA<br/>Did you do anything not required?"]
    A2_Q_ENTITLEMENT --> A2_Q_EXTRA
    
    A2_Q_EXTRA --> A2_D2["A2_D2<br/>Decision"]
    
    A2_D2 -->|Yes| A2_R_CONTRIB["A2_R_CONTRIB<br/>Reflection: Contribution"]
    A2_D2 -->|No| A2_R_ENTITLED["A2_R_ENTITLED<br/>Reflection: Entitled"]
    
    A2_R_CONTRIB --> BRIDGE_2_3["BRIDGE_2_3<br/>Bridge to Axis 3"]
    A2_R_ENTITLED --> BRIDGE_2_3
    
    BRIDGE_2_3 --> A3_OPEN["A3_OPEN<br/>Who comes to mind first?"]
    
    A3_OPEN --> A3_D1["A3_D1<br/>Decision"]
    
    A3_D1 -->|Self| A3_Q_SELF["A3_Q_SELF<br/>Did anyone else cross your mind?"]
    A3_D1 -->|Others| A3_Q_OTHER["A3_Q_OTHER<br/>What changed about your actions?"]
    
    A3_Q_SELF --> A3_D2["A3_D2<br/>Decision"]
    A3_Q_OTHER --> A3_D2
    
    A3_D2 -->|Emerging| A3_R_EMERGING["A3_R_EMERGING<br/>Reflection: Emerging"]
    A3_D2 -->|Self-Centric| A3_R_SELF["A3_R_SELF<br/>Reflection: Self-Centric"]
    A3_D2 -->|Altrocentric| A3_R_ALTROCENTRIC["A3_R_ALTROCENTRIC<br/>Reflection: Altrocentric"]
    
    A3_R_SELF --> SUMMARY["SUMMARY<br/>Conclusion"]
    A3_R_EMERGING --> SUMMARY
    A3_R_ALTROCENTRIC --> SUMMARY