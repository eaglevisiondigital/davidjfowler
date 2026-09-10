from pathlib import Path

root = Path(__file__).resolve().parents[1]
index_path = root / 'index.html'
styles_path = root / 'styles.css'

html = index_path.read_text(encoding='utf-8')

marker = '      <div id="schedule-list" class="schedule-list" aria-live="polite"></div>'
block = '''      <article class="faith-boost-schedule-card" aria-label="Daily Faith Boost Broadcast schedule">
        <div class="faith-boost-time">
          <span>DAILY</span>
          <strong>7 PM</strong>
          <small>CENTRAL</small>
        </div>
        <div class="faith-boost-schedule-copy">
          <p class="card-kicker">FAITH BOOST BROADCAST</p>
          <h3>Daily Faith Boost Broadcast</h3>
          <p>A daily shot in the arm to remind you who you are in Christ, what you have in Him, and what you can do through Him.</p>
        </div>
        <span class="faith-boost-live-badge">LIVE DAILY</span>
      </article>

      <div id="schedule-list" class="schedule-list" aria-live="polite"></div>'''

if 'faith-boost-schedule-card' not in html:
    if marker not in html:
        raise SystemExit('schedule-list marker not found')
    html = html.replace(marker, block, 1)
    index_path.write_text(html, encoding='utf-8')

css = styles_path.read_text(encoding='utf-8')
css_block = r'''

/* Faith Boost recurring schedule item */
.faith-boost-schedule-card{
  display:grid;
  grid-template-columns:118px 1fr auto;
  gap:24px;
  align-items:center;
  margin-bottom:16px;
  padding:22px 24px;
  border-radius:20px;
  background:
    radial-gradient(circle at 88% 10%,rgba(96,190,255,.14),transparent 30%),
    linear-gradient(135deg,rgba(13,43,78,.98),rgba(7,22,39,.98));
  border:1px solid rgba(100,184,255,.22);
  box-shadow:0 20px 50px rgba(0,0,0,.16);
}
.faith-boost-time{
  min-height:94px;
  border-radius:16px;
  background:linear-gradient(145deg,#153f72,#0b294c);
  display:flex;
  flex-direction:column;
  align-items:center;
  justify-content:center;
  border:1px solid rgba(255,255,255,.08);
}
.faith-boost-time span,
.faith-boost-time small{
  color:#8fc9ff;
  font-size:9px;
  font-weight:900;
  letter-spacing:.18em;
}
.faith-boost-time strong{
  color:#fff;
  font-size:27px;
  line-height:1.1;
  margin:3px 0;
}
.faith-boost-schedule-copy h3{
  margin:4px 0 6px;
  font-size:24px;
}
.faith-boost-schedule-copy p:not(.card-kicker){
  margin:0;
  color:#9eb5ca;
  max-width:850px;
}
.faith-boost-live-badge{
  padding:8px 11px;
  border-radius:999px;
  background:rgba(98,190,255,.1);
  border:1px solid rgba(98,190,255,.22);
  color:#7fc3ff;
  font-size:9px;
  font-weight:900;
  letter-spacing:.16em;
  white-space:nowrap;
}
@media(max-width:700px){
  .faith-boost-schedule-card{
    grid-template-columns:78px 1fr;
    gap:14px;
    padding:18px;
  }
  .faith-boost-time{
    min-height:82px;
  }
  .faith-boost-time strong{
    font-size:22px;
  }
  .faith-boost-schedule-copy h3{
    font-size:20px;
  }
  .faith-boost-schedule-copy p:not(.card-kicker){
    font-size:13px;
    line-height:1.55;
  }
  .faith-boost-live-badge{
    grid-column:2;
    justify-self:start;
  }
}
'''

if '/* Faith Boost recurring schedule item */' not in css:
    styles_path.write_text(css + css_block, encoding='utf-8')

print('Faith Boost recurring schedule item added.')
