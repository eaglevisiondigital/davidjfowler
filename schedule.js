// Healing revival schedule for David J. Fowler.
// Add exact venue/date details as they are publicly confirmed.

window.DJF_EVENTS = [
  {
    month: "SEP",
    day: "12",
    region: "HEALING REVIVAL",
    city: "Washington",
    state: "D.C.",
    venue: "Washington, D.C.",
    details: "September 12, 2026",
    url: ""
  },
  {
    month: "OCT",
    day: "10",
    region: "HEALING REVIVAL",
    city: "San Francisco",
    state: "CA",
    venue: "San Francisco, California",
    details: "October 10, 2026",
    url: ""
  },
  {
    month: "NOV",
    day: "2026",
    region: "HEALING REVIVAL",
    city: "New York City",
    state: "NY",
    venue: "New York City, New York",
    details: "November 2026",
    url: ""
  },
  {
    month: "DEC",
    day: "2026",
    region: "HEALING REVIVAL",
    city: "Seattle",
    state: "WA",
    venue: "Seattle, Washington",
    details: "December 2026",
    url: ""
  }
];

// Slim Faith Boost Broadcast promo beneath the three ministry cards.
// No external watch link is attached yet. When the permanent destination is chosen,
// this can be converted to a clickable banner without changing the layout.
(function addFaithBoostBanner() {
  const ministryGrid = document.querySelector('#ministry .ministry-grid');
  if (!ministryGrid || document.querySelector('.faith-boost-broadcast-banner')) return;

  const style = document.createElement('style');
  style.textContent = `
    .faith-boost-broadcast-banner {
      max-width: 1450px;
      min-height: 96px;
      margin: 20px auto 0;
      padding: 18px 26px;
      border: 1px solid rgba(111, 187, 255, .18);
      border-radius: 20px;
      background:
        radial-gradient(circle at 12% 50%, rgba(38, 137, 245, .13), transparent 30%),
        linear-gradient(110deg, rgba(10, 27, 47, .98), rgba(7, 18, 32, .98));
      box-shadow: 0 18px 42px rgba(0, 0, 0, .18);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 28px;
      overflow: hidden;
      position: relative;
    }
    .faith-boost-broadcast-banner::before {
      content: '';
      position: absolute;
      left: 0;
      top: 0;
      bottom: 0;
      width: 4px;
      background: linear-gradient(180deg, #69b7ff, #e2b45b);
    }
    .faith-boost-broadcast-banner__copy {
      min-width: 0;
    }
    .faith-boost-broadcast-banner__label {
      margin: 0 0 3px;
      color: #6db7ff;
      font-size: 10px;
      font-weight: 900;
      letter-spacing: .22em;
    }
    .faith-boost-broadcast-banner__title {
      margin: 0;
      color: #f5f8fb;
      font-size: clamp(20px, 2vw, 29px);
      line-height: 1.12;
      letter-spacing: -.025em;
    }
    .faith-boost-broadcast-banner__title strong {
      color: #f0be62;
    }
    .faith-boost-broadcast-banner__time {
      flex: 0 0 auto;
      display: inline-flex;
      align-items: center;
      gap: 9px;
      padding: 11px 16px;
      border-radius: 999px;
      border: 1px solid rgba(240, 190, 98, .24);
      background: rgba(240, 190, 98, .07);
      color: #f5d18c;
      font-size: 11px;
      font-weight: 900;
      letter-spacing: .11em;
      white-space: nowrap;
    }
    .faith-boost-broadcast-banner__live-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #ff6262;
      box-shadow: 0 0 12px rgba(255, 98, 98, .65);
    }
    @media (max-width: 700px) {
      .faith-boost-broadcast-banner {
        min-height: 0;
        padding: 18px 20px;
        margin-top: 16px;
        border-radius: 18px;
        align-items: flex-start;
        flex-direction: column;
        gap: 13px;
      }
      .faith-boost-broadcast-banner__title {
        font-size: 21px;
      }
      .faith-boost-broadcast-banner__time {
        padding: 9px 13px;
        font-size: 10px;
      }
    }
  `;
  document.head.appendChild(style);

  const banner = document.createElement('div');
  banner.className = 'faith-boost-broadcast-banner';
  banner.setAttribute('aria-label', 'Faith Boost Broadcast live daily at 7 PM Central Time');
  banner.innerHTML = `
    <div class="faith-boost-broadcast-banner__copy">
      <p class="faith-boost-broadcast-banner__label">FAITH BOOST BROADCAST</p>
      <p class="faith-boost-broadcast-banner__title">Be sure to tune in <strong>live daily</strong> for your Faith Boost.</p>
    </div>
    <div class="faith-boost-broadcast-banner__time">
      <span class="faith-boost-broadcast-banner__live-dot" aria-hidden="true"></span>
      7 PM CENTRAL TIME
    </div>
  `;

  ministryGrid.insertAdjacentElement('afterend', banner);
})();
