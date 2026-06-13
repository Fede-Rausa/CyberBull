def css_style_str():
    return """
<style>
:root {
    --surface:  #1c1f2b;
    --border:   #2a2d3e;
    --accent:   #7c6af7;
    --accent2:  #a78bfa;
    --text:     #e2e8f0;
    --text-dim: #94a3b8;
    --green:    #34d399;
    --bg:          #0f1117;
    --surface:     #1c1f2b;
    --surface2:    #13162080;
    --border:      #2a2d3e;
    --accent:      #7c6af7;
    --accent2:     #a78bfa;
    --muted:       #6b7280;
    --text:        #e2e8f0;
    --text-dim:    #94a3b8;
    --green:       #34d399;
    --bubble-me:   #4c3fb5;
    --bubble-them: #252840;
}


#MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    /* Hide only the right-side toolbar buttons (deploy, fork, github) */
    [data-testid="stToolbarActions"] {visibility: hidden;}


.post-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 14px; padding: 18px 22px; margin-bottom: 14px;
    transition: border-color .15s;
}
.post-card:hover { border-color: var(--accent); }
.post-author {
    font-weight: 700; font-size: .92rem; color: var(--accent2);
}
.post-meta {
    font-size: .75rem; color: var(--text-dim); margin-bottom: 10px;
}
.author-avatar {
    width: 32px; height: 32px; border-radius: 50%;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    display: inline-flex; align-items: center; justify-content: center;
    font-size: .8rem; font-weight: 700; color: #fff;
    margin-right: 8px; vertical-align: middle;
}
.post-divider { border: none; border-top: 1px solid var(--border); margin: 6px 0 12px; }
.filter-bar { margin-bottom: 18px; }
.empty-state { color: var(--text-dim); font-size: .9rem; text-align: center; padding: 40px 0; }



.block-container {padding-top: 3.5rem; padding-bottom: 2rem;}
.sec-header {
    font-size: 1.35rem; 
    font-weight: 700; 
    color: #0f172a; /* Deep slate black—modern and highly readable */
    border-bottom: 1px solid #e2e8f0; /* Soft, clean light gray divider */
    padding-bottom: 10px; 
    margin-bottom: 20px;
}
.section-label {
    font-size: .75rem; 
    font-weight: 700; 
    letter-spacing: .08em;
    text-transform: uppercase; 
    color: #64748b; /* Soft slate gray - highly readable but secondary */
    margin: 20px 0 8px;
}
.card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 14px; padding: 22px 26px; margin-bottom: 20px;
}
.avatar-lg {
    width: 80px; height: 80px; border-radius: 50%;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    display: flex; align-items: center; justify-content: center;
    font-size: 2rem; font-weight: 700; color: #fff; margin-bottom: 12px;
}


.block-container {padding-top: 3.5rem; padding-bottom: 2rem;}

.contact-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; padding: 14px 18px; margin-bottom: 4px;
    display: flex; align-items: center; gap: 14px; transition: border-color .15s;
}
.contact-card:hover { border-color: var(--accent); }
.avatar {
    width: 42px; height: 42px; border-radius: 50%;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 1rem; color: #fff; flex-shrink: 0;
}
.contact-name { font-weight: 600; font-size: 1rem; color: var(--text); }
.friend-badge {
    font-size: .7rem; padding: 2px 8px; border-radius: 99px;
    background: #1a3a2a; color: var(--green); border: 1px solid var(--green);
    margin-left: 8px; vertical-align: middle;
}
.chat-wrap { display: flex; flex-direction: column; gap: 8px; margin-bottom: 20px; }
.bubble-row { display: flex; }
.bubble-row.me   { justify-content: flex-end; }
.bubble-row.them { justify-content: flex-start; }
.bubble {
    max-width: 68%; padding: 10px 14px; border-radius: 16px;
    font-size: .92rem; line-height: 1.45; color: var(--text);
}
.bubble.me   { background: var(--bubble-me);   border-bottom-right-radius: 4px; }
.bubble.them { background: var(--bubble-them); border-bottom-left-radius: 4px; }
.bubble-meta { font-size: .7rem; color: var(--text-dim); margin-top: 2px; }
.bubble-row.me .bubble-meta { text-align: right; }
.sec-header {
    font-size: 1.35rem; font-weight: 700; color: var(--text);
    border-bottom: 1px solid var(--border); padding-bottom: 10px; margin-bottom: 18px;
}
.sub-text { color: var(--text-dim); font-size: .88rem; }
.profile-box {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 16px; padding: 28px 32px; max-width: 620px;
}
.profile-avatar {
    width: 72px; height: 72px; border-radius: 50%;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    display: flex; align-items: center; justify-content: center;
    font-size: 1.8rem; font-weight: 700; color: #fff; margin-bottom: 14px;
}
.profile-desc {
    background: var(--surface2); border-radius: 10px; padding: 14px 16px;
    color: var(--text-dim); font-size: .93rem; line-height: 1.6;
    border: 1px solid var(--border); margin-top: 10px;
}


.pref-pill {
    display: inline-block; 
    background: rgba(99, 102, 241, 0.1); /* 10% opacity Indigo */
    border: 1px solid rgba(99, 102, 241, 0.3); /* 30% opacity Indigo border */
    border-radius: 99px;
    padding: 4px 14px; 
    font-size: .85rem; 
    color: #818cf8; /* Bright, legible indigo text */
    margin: 4px 4px 4px 0;
    transition: background 0.2s ease;
}

/* Optional hover effect if they are clickable */
.pref-pill:hover {
    background: rgba(99, 102, 241, 0.2);
    cursor: pointer;
}
.post-card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; padding: 16px 20px; margin-bottom: 12px;
}
.post-meta { font-size: .75rem; color: var(--text-dim); margin-bottom: 8px; }
.profile-desc {
    background: #1a1d29; /* Solid dark background instead of semi-transparent */
    border-radius: 10px; 
    padding: 14px 16px;
    color: #e2e8f0; /* Crisp, off-white for excellent readability */
    font-size: .93rem; 
    line-height: 1.6;
    border: 1px solid #2d3142; /* Defined, subtle border */
}
</style>

"""