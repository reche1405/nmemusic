from core.models import db 
from core.models.page import Page, Section
from core.models.service import Service
from core.models.event import Event
from core.models.genre import Genre
from core.models.policy import Policy
from core.app import create_app
from datetime import date, datetime, timedelta
from slugify import slugify


page_data = [
    {
        'title': 'Welcome to NME Music',
        'description' : 'NME Music have 20+ years of combined experience in building large scale festivals, concerts & events from the ground up.',
        'keywords' : "NME Music, Hastings Festivals, Eastbourne Festivals, Music Events Hastings, London Nightlife",
        'tag' : 'home',
    },
    {
        'title': 'About NME Music | Our Story & Vision',
        'description': 'Discover the team behind the noise. With over two decades of industry expertise, we turn ambitious event concepts into unforgettable live music realities.',
        'keywords': "About NME Music, Event Organizers Sussex, Music Festival Creators, Live Music Production Team",
        'tag': 'about',
    },
    {
        'title': 'Upcoming Festivals & Music Events | NME Music',
        'description': 'Check out our latest lineup of upcoming music festivals, concerts, and nightlife events across Hastings, Eastbourne, and London.',
        'keywords': "NME Music Events, Live Concerts Hastings, Upcoming Festivals 2026, London Club Nights",
        'tag': 'events',
    },
    {
        'title': 'NME Music Gallery | Relive the Experience',
        'description': 'Browse through our crowd-voted highlights, artist photos, and official event galleries capturing the energy of our past festivals and shows.',
        'keywords': "Festival Photos, NME Music Gallery, Concert Photography, Live Event Pictures",
        'tag': 'gallery',
    },
    {
        'title': 'Contact NME Music | Get In Touch',
        'description': 'Want to collaborate, book us, or have a question about an upcoming event? Reach out to the NME Music team today.',
        'keywords': "Contact NME Music, Festival Booking, Event Management Inquiry, Music Promotion Support",
        'tag': 'contact',
    },
    {
    'title': 'Event Management & Hosting Services | NME Music',
    'description': 'Explore NME Music/’s full range of event hosting, production, and management services. From intimate showcases to large-scale festivals, we bring your vision to life.',
    'keywords': 'Event Management Services, Festival Production, Live Event Hosting, Corporate Event Planning, Music Event Coordination',
    'tag': 'services',
    }

]

section_data = [
    {
        "page_id" : 1, 
        "title" : "Brigning Unforgettable Music Experiences to the UK",
        "subtitle" : "NME Music",
        "tag" : "home-intro"
    },
    {
        "page_id" : 1, 
        "subtitle" : "NME Music",
        "text" : "At NME Music, we’re passionate about delivering diverse and immersive music experiences. From intimate club nights to large-scale festivals and live concerts. Our mission is to curate unforgettable moments that unite people through the power of music.",
        "tag" : "home-passion",
    },
    {
        "page_id" : 1, 
        "subtitle" : "NME Music",
        "text" : "See what's in store, explore our previous events and relive the magic!",
        "tag" : "home-explore",
    },
    {
        "page_id" : 1, 
        "title" : "What's Next?",
        "tag" : "home-next",
    },
    {
        "page_id" : 2, 
        "title" : "Who We Are",
        "text" : "At JBM Music, we’re more than just event organisers—we’re a passionate team of music lovers,"
            "reatives, and industry experts dedicated to crafting unforgettable experiences.",
        "tag" : "about-who",
    },
     {
        "page_id" : 2, 
        "title" : "Industry Experience",
        "text" : "With 25 years of combined"
            "expertise, we specialise in bringing world-class music events to life, from festivals and concerts to"
            "club nights and live shows.\n",
        "tag" : "about-experience",
    },
    {
        "page_id" : 2, 
        "title" : "Total Event Management",
        "text" : "Our in-house team is the heartbeat of everything we do, expertly"
            "managing artist bookings, logistics, marketing, and creative direction to ensure every event runs"
            "seamlessly.\n We collaborate with globally renowned artists and emerging talent across all genres,"
            "curating diverse line-ups that cater to every music lover. At JBM Music, our mission is simple—combine our"
            "expertise and passion to create events that leave a lasting impression.",
        "tag" : "about-in-house",
    },
    {
        "page_id" : 2, 
        "title" : "What'We Do",
        "text" : "We are a full-service events company, creating, managing, operating and promoting live music events and festivals across the UK. Our in-house team handles everything from artist booking and logistics to marketing and event delivery, ensuring every show runs seamlessly from start to finish.\n\
With expertise across multiple genres, we curate and produce unforgettable experiences tailored to each event and its audience. From sourcing world-class talent to executing flawless production, we take care of every detail—bringing exceptional music events to life, time and time again.\n\
Get in touch today to start a conversation on how we can work together, to deliver exceptional events. ",
        "tag" : "about-what",
    },
]


genre_data = [
    {'title' : 'DnB'},
    {'title' : 'Dubstep'},
    {'title' : 'House'},
    {'title' : 'Garage'},
    {'title' : 'Reggae'},
    {'title' : 'Grime'},
    {'title' : 'Dancehall'},
]

event_data = [
    {
        'location': 'Milton Keynes Stadium MK',
        'date' : date.today() - timedelta(days=365),
        'ticket_link' : 'https://skiddle.com/events?id=123940569304',
        'title' : 'ANDY C - BASSJAM',
        'short_desc': 'Get ready for an electric night of drum and bass as the legendary Andy C headlines Bassjam at Milton Keynes Stadium MK.\nExpect heavy baselines, breathtaking visuals, and high-energy festival production that will keep you dancing all night long.',
    },
    {
        'location': 'Milton Keynes Stadium MK',
        'date' : date.today() - timedelta(days=665),
        'ticket_link' : 'https://skiddle.com/events?id=123940359302',
        'title' : 'CAMELPHAT - BLOW',
        'short_desc': 'CamelPhat and Andy C unite for an unforgettable night of electronic excellence at Milton Keynes Stadium MK.\nExperience the perfect fusion of house and drum and bass, with world-class production, pulsating beats, and an electric atmosphere that will keep you dancing until dawn.',
    },
    {
        'location': 'Hastings Pier',
        'date' : date.today() - timedelta(days=724),
        'ticket_link' : 'https://skiddle.com/events?id=452740569901',
        'title' : 'GARAGE NATION',
        'short_desc': 'The ultimate celebration of UK Garage music takes over Hastings Pier for a massive, nostalgia-fueled showcase.\nFeaturing a huge lineup of legendary MCs and DJs, this event brings the finest old-school anthems and garage riddims back to life.',
    },
    {
        'location': 'The Oval, Hastings',
        'date' : date.today() - timedelta(days=1065),
        'ticket_link' : 'https://skiddle.com/events?id=958687569789',
        'title' : 'REGGAE FESTIVAL',
        'short_desc': 'Experience the ultimate summer soundtrack as Hastings Reggae Festival brings sunny, positive vibrations to the arena stadium grounds.\nImmerse yourself in a diverse lineup of live reggae, roots, and dub artists paired with great food and a relaxed, community festival vibe.',
    },
   
]

service_data = [
    {
        'title': 'Event Security',
        'slug': 'event-security',
        'short_desc': 'Comprehensive event security and crowd management services across the UK. Professional, SIA-licensed security personnel from ProFM Group ensuring safety, compliance, and total peace of mind.',
        'long_desc': (
            "Comprehensive, premier event security and crowd management services across the UK. At ProFM Group, we "
            "understand that safeguarding your guests, staff, and assets is the single most critical element of any successful "
            "gathering. Our elite team of SIA-licensed security professionals is rigorously trained to handle the unique "
            "dynamics of large-scale music festivals, high-profile corporate galas, intimate VIP gatherings, and massive sports "
            "stadium events. We don't just provide a physical presence; we deliver a complete, tailored security ecosystem designed "
            "to seamlessly blend into your event's operational flow.\n\n"
            "Our approach begins long before the gates open. We collaborate closely with event organizers, local authorities, and "
            "emergency services to conduct exhaustive risk assessments, draft detailed crowd management strategies, and implement "
            "robust emergency protocols. On-site, our personnel excel in counter-terrorism awareness, conflict resolution, threat "
            "detection, and perimeter protection. We utilize advanced communication networks and real-time monitoring to mitigate "
            "risks swiftly and discreetly, maintaining total operational control from start to finish.\n\n"
            "Beyond tactical excellence, we place a massive emphasis on front-of-house customer service. Our security officers act "
            "as an extension of your brand, greeting attendees with a welcoming yet authoritative demeanor. By balancing ironclad "
            "protection with polite, professional public interaction, we ensure that safety compliance never compromises the guest "
            "experience. Partner with us to guarantee complete operational compliance, strict asset protection, and total peace of "
            "mind for your next major event."
        )
    },
    {
        'title': 'Event Stewards',
        'slug': 'event-stewards',
        'short_desc': 'Friendly, professional, and highly trained event stewards to assist with crowd control, guest guidance, and customer service, ensuring your event runs smoothly and safely.',
        'long_desc': (
            "Friendly, professional, and highly capable event stewarding services designed to keep your venue organized, accessible, "
            "and perfectly coordinated. While security personnel handle critical threats, our stewarding teams serve as the vital "
            "backbone of public safety, guest guidance, and logistical fluidity. Trained extensively in customer care, crowd dynamics, "
            "and venue layout navigation, our stewards ensure that every attendee enjoys a smooth, stress-free journey from the "
            "moment they arrive at your perimeter.\n\n"
            "Our stewards are multi-skilled assets deployment-ready for a vast array of crucial responsibilities. They manage main "
            "ingress and egress points, execute efficient ticket scanning and wristband checking, guide vehicular traffic in parking "
            "zones, and oversee dedicated seating bowl management. In addition, they maintain a highly visible presence throughout "
            "the venue, acting as the primary point of contact for guest inquiries, lost property, and general assistance, which "
            "drastically reduces the burden on your core management team.\n\n"
            "Safety remains at the heart of our stewarding operations. Every team member is deeply briefed on the specific evacuation "
            "routes, first-aid locations, and emergency procedures of your venue. In the rare event of an incident, our stewards "
            "act as calm, clear-headed leaders, efficiently directing crowds and assisting emergency services. With ProFM Group, you "
            "receive a passionate hospitality-driven workforce that keeps your event moving forward safely, efficiently, and with "
            "a smile."
        )
    },
    {
        'title': 'Bar Staff',
        'slug': 'bar-staff',
        'short_desc': 'Experienced, fast-paced, and hospitality-focused bar staff and mixologists. Fully trained to handle high-volume event bars while maintaining exceptional customer service.',
        'long_desc': (
            "Elite, high-energy hospitality teams and professional bar staffing solutions tailored to maximize beverage revenue and "
            "elevate the guest experience. High-volume event bars are notorious pressure cookers where slow service directly impacts "
            "your bottom line and fuels crowd frustration. ProFM Group eliminates these bottlenecks by providing exceptionally trained, "
            "fast-paced bar operators, supervisors, and mixologists who thrive under the intense demands of festival arenas, arena "
            "concerts, and corporate functions.\n\n"
            "Every member of our bar staff undergoes rigorous training encompassing speed-pouring techniques, menu memorization, asset "
            "stock control, and strict licensing compliance. We ensure all personnel are fully versed in local alcohol weights and "
            "measures legislation, as well as robust underage sales prevention protocols like Challenge 25. Our supervisors monitor "
            "pour wastage and inventory levels in real-time, protecting your profit margins while maintaining an impeccable standard "
            "of hygiene and bar presentation.\n\n"
            "We believe that speed should never come at the expense of hospitality. Our staff are selected not just for their technical "
            "skills, but for their charismatic personalities and ability to engage positively with patrons under pressure. From crafting "
            "complex bespoke cocktails at high-end VIP lounges to crushing high-volume draft volumes at main-stage beer tents, our "
            "teams deliver premium, profitable, and memorable beverage operations."
        )
    },
    {
        'title': 'Stage Design',
        'slug': 'stage-design',
        'short_desc': 'Bespoke stage design and production services. From conceptual 3D renders to structural builds, we create visually stunning main stages tailored to your event theme and artist requirements.',
        'long_desc': (
            "Innovative, bespoke stage design and full-scale structural production services engineered to transform creative visions "
            "into jaw-dropping live realities. The stage is the literal focal point of your event; it tells your story and frames the "
            "entire artistic performance. Our world-class design team collaborates with you from day one, turning initial conceptual "
            "mood boards into highly detailed 3D CAD renders, structural blueprints, and material specifications tailored to your "
            "exact aesthetic goals.\n\n"
            "We handle the entire structural life cycle, ensuring that stunning visual artistry is perfectly backed by rigorous "
            "structural engineering. Our build teams manage the sourcing, transport, and assembly of heavy-duty stage scaffolding, "
            "custom scenic carpentry, integrated video walls, and specialized rigging structures. Whether you require an intimate, "
            "branding-heavy corporate seminar stage or a massive, multi-tiered outdoor festival main stage built to withstand unpredictable "
            "weather elements, we build to the highest safety and architectural standards.\n\n"
            "Furthermore, our designs are built with practical performance logistics in mind. We actively coordinate with incoming artist "
            "management teams to accommodate complex tech riders, quick changeovers, sub-stage prop storage, and optimized viewing angles. "
            "By choosing ProFM Group, you unlock a breathtaking, structurally sound centerpiece that captivates audiences, satisfies "
            "performing talent, and elevates your event's overall production value."
        )
    },
    {
        'title': 'Marketing',
        'slug': 'marketing',
        'short_desc': 'Data-driven event marketing, digital campaigns, and PR strategies designed to boost ticket sales, maximize brand awareness, and engage your target audience effectively.',
        'long_desc': (
            "Cutting-edge, data-driven event marketing campaigns and comprehensive PR strategies designed to ignite brand awareness, "
            "drive ticket sales, and foster lasting fan loyalty. In a crowded entertainment marketplace, breaking through the noise "
            "requires a calculated blend of digital precision and creative storytelling. Our specialized marketing department analyzes "
            "your target demographic to construct aggressive multi-channel campaigns that convert casual scrollers into passionate "
            "ticket buyers.\n\n"
            "Our scope covers the full spectrum of modern digital marketing, including advanced paid social media advertising (Meta, "
            "TikTok, Google Ads), targeted search engine optimization, programmatic media buying, and high-impact email marketing loops. "
            "We don't believe in vanity metrics; we track real-time cost-per-acquisition and conversion data, continuously optimizing "
            "ad spend to achieve maximum return on investment. Alongside paid ads, we manage community building, engaging organic content "
            "creation, and high-profile influencer partnerships.\n\n"
            "Beyond the digital realm, we execute traditional PR, local guerrilla marketing, and strategic media placements to build "
            "widespread hype. From initial announcement phases and early-bird ticket drops to last-minute final releases and on-site "
            "live coverage, we provide continuous momentum. Let us handle the complexities of audience acquisition so you can focus "
            "on delivering an unforgettable event to a completely sold-out crowd."
        )
    },
    {
        'title': 'Talent Procurement',
        'slug': 'talent-procurement',
        'short_desc': 'End-to-end artist and talent booking services. Leveraging industry relationships to secure top-tier DJs, live acts, and hosts while managing contracts, riders, and logistics.',
        'long_desc': (
            "End-to-end artist booking and talent procurement services leveraging deep entertainment industry networks to secure the "
            "perfect talent lineup for your budget. Booking headline talent, international DJs, or elite keynote speakers can be a "
            "minefield of complex contracts, inflated agency rates, and demanding hospitality riders. ProFM Group acts as your expert "
            "intermediary, protecting your financial interests while aligning your event with world-class performers.\n\n"
            "Our experienced talent bookers handle the entire negotiation pipeline. We manage initial availability checks, pitch "
            "compelling event concepts to major global talent agencies, and aggressively negotiate performance fees to maximize your "
            "budget. Once an artist is secured, we dive deep into legal contract administration, carefully reviewing and refining "
            "billing order, performance times, marketing rights, cancellation policies, and intricate technical and hospitality "
            "riders to eliminate hidden costs.\n\n"
            "Our job doesn't end when the contract is signed. We provide comprehensive artist liaison services, managing complex ground "
            "transportation, hotel accommodations, backstage dressing room dressing, and dedicated on-site hospitality managers. We "
            "ensure your talent feels respected, relaxed, and fully prepared to deliver a flawless show, while seamlessly shielding "
            "you from the stressful logistics of artist management."
        )
    },
    {
        'title': 'Equipment & Lighting',
        'slug': 'equipment-lighting',
        'short_desc': 'Premium audio-visual installations, pro-grade sound systems, and immersive lighting rigs. Full technical support and equipment hire to elevate production value.',
        'long_desc': (
            "Premium, touring-grade audio-visual equipment hire and state-of-the-art lighting production designed to create truly "
            "immersive sensory environments. Sound and light are the emotional conductors of any live experience; crisp audio and "
            "dynamic lighting can transform a standard venue into a breathtaking spectacle. ProFM Group supplies an extensive inventory "
            "of top-tier technical hardware, giving you access to the same equipment used on major global stadium tours.\n\n"
            "Our audio division provides pristine, high-fidelity sound systems, including advanced line-array speakers, digital mixing "
            "consoles, and pro-grade wireless microphone systems tailored to the unique acoustics of your space. Simultaneously, our "
            "lighting inventory boasts cutting-edge moving head fixtures, strobe lights, laser systems, and high-density LED video panels. "
            "Whether you need crystal-clear speech intelligibility for a corporate keynote or a earth-shaking, synchronized light-and-sound "
            "spectacle for an electronic music festival, we have the gear to deliver.\n\n"
            "We don't just rent hardware; we provide complete technical peace of mind. Our team of certified sound engineers, lighting "
            "designers, and master electricians handle the full setup, power distribution, real-time show operation, and efficient "
            "strike. With strict adherence to safety regulations and meticulous equipment maintenance, we guarantee a flawless technical "
            "execution free from dropouts or glitches."
        )
    }
]

policy_data = [
    {
    'title' : 'Privacy Policy',
    'slug' : 'privacy-policy',
    'intro' : 'We are committed to protecting your privacy and handling your personal data transparently and securely in accordance with UK GDPR',
    'body' : """


<div class="content">

  <h1>Privacy Policy · NME Music</h1>
  <p style="color: #475569; margin-top: -0.8rem; font-weight: 500;"><span class="badge">UK GDPR compliant</span> Last Updated: <strong>20 July 2026</strong></p>

  <!-- 1. Who We Are -->
  <h2>1. Who We Are</h2>
  <p>NME Music is a UK-based event hosting and management company. We organise our own events and provide event management services to our clients. We are committed to protecting your privacy and handling your personal data transparently and securely in accordance with the UK General Data Protection Regulation (UK GDPR) and the Data Protection Act 2018.</p>
  <p>For the purposes of data protection law, NME Music is the Data Controller for the personal data we collect and process for our own business purposes.</p>

  <div class="contact-block">
    <p><strong>Our Contact Details:</strong></p>
    <p><strong>Company Name:</strong> NME Music</p>
    <p><strong>Email Address:</strong> <a href="mailto:info@nmemusic.co.uk">info@nmemusic.co.uk</a></p>
    <p><strong>Address:</strong> [Insert your registered business address]</p>
    <p style="margin-top: 0.5rem;">If you have any questions about this Privacy Policy or how we handle your personal data, please contact us using the details above.</p>
  </div>

  <!-- 2. Scope -->
  <h2>2. Scope of This Policy</h2>
  <p>This Privacy Policy applies to personal data we collect:</p>
  <ul>
    <li>When you use our website.</li>
    <li>When you register for, attend, or participate in events we host or manage.</li>
    <li>When you use our event management services as a client.</li>
    <li>When you contact us by email, phone, or post.</li>
    <li>When you subscribe to our mailing list or marketing communications.</li>
  </ul>
  <p>This Policy does not apply when we process personal data on behalf of our clients as a Data Processor. In those circumstances, our client is the Data Controller, and their privacy policy will apply.</p>

  <!-- 3. Personal Data -->
  <h2>3. The Personal Data We Collect</h2>
  <p>Depending on your relationship with us, we may collect the following types of personal data:</p>

  <h3>A. Event Attendees &amp; Guests</h3>
  <ul>
    <li><strong>Contact Data:</strong> Full name, email address, postal address, and telephone number.</li>
    <li><strong>Booking &amp; Attendance Data:</strong> Ticket purchase information, event preferences, attendance records, and dietary or access requirements (which may constitute special category data).</li>
    <li><strong>Payment Data:</strong> Billing address and payment card details (processed securely by our third-party payment processors; we do not store full payment card details).</li>
    <li><strong>Profile Data:</strong> Information you choose to provide, such as preferences, feedback, and survey responses.</li>
  </ul>

  <h3>B. Clients &amp; Business Contacts</h3>
  <ul>
    <li><strong>Contact Data:</strong> Name, job title, business email address, business phone number, and company address.</li>
    <li><strong>Contract &amp; Transaction Data:</strong> Details about contracts, services provided, invoices, and payment history.</li>
    <li><strong>Communication Data:</strong> Records of correspondence and interactions with us.</li>
  </ul>

  <h3>C. Website Visitors</h3>
  <ul>
    <li><strong>Technical Data:</strong> IP address, browser type and version, time zone setting, browser plug-in types and versions, operating system and platform, and other technology on the devices you use to access our website.</li>
    <li><strong>Usage Data:</strong> Information about your visit, including pages viewed, clickstream data, and length of sessions.</li>
  </ul>

  <h3>D. Job Applicants</h3>
  <ul>
    <li><strong>Recruitment Data:</strong> Information included in your CV, such as name, contact details, employment history, qualifications, and references.</li>
  </ul>

  <!-- 4. How we collect -->
  <h2>4. How We Collect Your Data</h2>
  <p>We collect personal data through the following means:</p>
  <ul>
    <li><strong>Direct Interactions:</strong> When you register for an event, enquire about our services, contact us directly, or enter into a contract with us.</li>
    <li><strong>Automated Technologies:</strong> When you visit our website, we may automatically collect Technical and Usage Data via cookies and similar technologies (please see our separate <strong>Cookie Policy</strong> for more details).</li>
    <li><strong>Third Parties:</strong> We may receive data from ticketing platforms, or from partners we work with to co-host events.</li>
  </ul>

  <!-- 5. Legal basis -->
  <h2>5. How We Use Your Data and the Legal Basis</h2>
  <p>We will only use your personal data when the law allows us to. The legal bases we rely on are:</p>
  <ul>
    <li><strong>Contractual Necessity:</strong> To perform a contract with you (e.g., providing event management services, processing event registrations) or to take steps at your request before entering into a contract (UK GDPR Art. 6(1)(b)).</li>
    <li><strong>Legitimate Interests:</strong> For our legitimate business interests, such as managing our business relationships, improving our services, and direct marketing (provided these interests are not overridden by your rights) (UK GDPR Art. 6(1)(f)).</li>
    <li><strong>Legal Obligation:</strong> To comply with a legal obligation, such as tax, accounting, or regulatory requirements (UK GDPR Art. 6(1)(c)).</li>
    <li><strong>Consent:</strong> Where you have given us clear consent to process your data for a specific purpose, such as sending you marketing communications (UK GDPR Art. 6(1)(a)). You may withdraw your consent at any time.</li>
  </ul>

  <!-- 6. Purposes table -->
  <h2>6. Purposes of Processing</h2>
  <p>We use your personal data for the following purposes:</p>
  <table>
    <thead>
      <tr><th>Purpose</th><th>Data Categories</th><th>Legal Basis</th></tr>
    </thead>
    <tbody>
      <tr><td>Deliver and administer our event hosting and management services to clients.</td><td>Contact, Contract, Transaction, Communication</td><td>Contractual Necessity / Legitimate Interests</td></tr>
      <tr><td>Register attendees for events, facilitate attendance, and manage logistics.</td><td>Contact, Booking &amp; Attendance, Payment, Profile</td><td>Contractual Necessity / Legitimate Interests / Consent (for special category data)</td></tr>
      <tr><td>Manage our commercial relationship with you (e.g., billing, client support).</td><td>Contact, Contract, Transaction, Communication</td><td>Contractual Necessity / Legal Obligation</td></tr>
      <tr><td>Send you marketing communications about our services and events, where you have provided consent or where we rely on legitimate interests.</td><td>Contact, Marketing &amp; Communications</td><td>Consent / Legitimate Interests</td></tr>
      <tr><td>Improve our website, services, and user experience through analytics.</td><td>Technical, Usage</td><td>Legitimate Interests</td></tr>
      <tr><td>Comply with applicable laws and regulations (e.g., tax, health and safety, insurance).</td><td>Contact, Transaction, Special Category (if applicable)</td><td>Legal Obligation / Legitimate Interests</td></tr>
      <tr><td>Detect, prevent, and investigate fraud and security incidents.</td><td>Contact, Technical</td><td>Legitimate Interests / Legal Obligation</td></tr>
    </tbody>
  </table>

  <!-- 7. Sharing -->
  <h2>7. Sharing and Disclosure of Personal Data</h2>
  <p>We do not sell your personal data to third parties. We may share your data in the following circumstances:</p>
  <ul>
    <li><strong>Service Providers &amp; Processors:</strong> We engage trusted third-party suppliers who process data on our behalf, such as ticketing platforms, IT systems providers, payment processors, email marketing platforms, and analytics providers. These suppliers are bound by data processing agreements and may only process your data on our instructions.</li>
    <li><strong>Business Partners:</strong> Where necessary to deliver our services, we may share data with co-organisers, venues, or other event partners. We will ensure appropriate contractual protections are in place.</li>
    <li><strong>Legal &amp; Regulatory Authorities:</strong> We may disclose data where required by law, court order, or regulation, or where necessary to protect our legal rights or the rights of others.</li>
    <li><strong>Business Transfers:</strong> In the event of a merger, acquisition, or sale of assets, personal data may be transferred as part of that transaction.</li>
  </ul>

  <!-- 8. International -->
  <h2>8. International Transfers of Personal Data</h2>
  <p>Your personal data may be transferred to, and processed in, countries outside the United Kingdom (UK). Some of our third-party service providers operate outside the UK.</p>
  <p>Where we transfer personal data internationally, we ensure that appropriate safeguards are in place in accordance with the UK GDPR, such as:</p>
  <ul>
    <li>Transfers to countries which the UK Secretary of State has determined to offer an adequate level of data protection.</li>
    <li>Use of UK International Data Transfer Agreements (IDTAs) or UK Addenda to the EU Standard Contractual Clauses.</li>
  </ul>
  <p>You may request further information about the specific safeguards in place for any international transfer by contacting us at <a href="mailto:info@nmemusic.co.uk">info@nmemusic.co.uk</a>.</p>

  <!-- 9. Retention -->
  <h2>9. Data Retention</h2>
  <p>We will only retain your personal data for as long as necessary to fulfil the purposes we collected it for, including for the purposes of satisfying any legal, accounting, or reporting obligations.</p>
  <p>Our general retention periods are:</p>
  <ul>
    <li><strong>Client &amp; Contract Records:</strong> Up to 7 years from the end of the commercial relationship (to comply with statutory limitation periods and tax obligations).</li>
    <li><strong>Prospect &amp; Marketing Contact Records:</strong> Until you unsubscribe or withdraw consent, or up to 3 years from the last interaction.</li>
    <li><strong>Event Attendee Data:</strong> Up to 3 years after the event for administrative and feedback purposes.</li>
    <li><strong>Website Analytics Data:</strong> Up to 26 months from collection (standard analytics tool retention).</li>
    <li><strong>Correspondence &amp; Enquiry Records:</strong> Up to 3 years from the last contact.</li>
  </ul>

  <!-- 10. Your rights -->
  <h2>10. Your Rights</h2>
  <p>Under the UK GDPR and the Data Protection Act 2018, you have the following rights regarding your personal data:</p>
  <ul>
    <li><strong>Right of Access (Subject Access Request):</strong> You have the right to request a copy of the personal data we hold about you, together with information about how and why we process it.</li>
    <li><strong>Right to Rectification:</strong> You have the right to request correction of inaccurate personal data or completion of incomplete data.</li>
    <li><strong>Right to Erasure (‘Right to be Forgotten’):</strong> You may request deletion of your personal data where there is no compelling reason for its continued processing (this right is not absolute and may be limited by legal obligations).</li>
    <li><strong>Right to Restriction of Processing:</strong> You may request that we restrict the processing of your data in certain circumstances, for example while a complaint is being investigated.</li>
    <li><strong>Right to Data Portability:</strong> You may request that we provide your data in a structured, commonly used, machine-readable format.</li>
    <li><strong>Right to Object:</strong> You have the right to object to processing based on our legitimate interests, and to object to the use of your personal data for direct marketing purposes at any time.</li>
    <li><strong>Right to Withdraw Consent:</strong> Where we rely on consent as the legal basis for processing, you may withdraw that consent at any time.</li>
  </ul>
  <p>To exercise any of these rights, please contact us at <a href="mailto:info@nmemusic.co.uk"><strong>info@nmemusic.co.uk</strong></a>. We will not charge a fee for handling a rights request and will respond within one calendar month. You also have the right to lodge a complaint with the UK Information Commissioner’s Office (ICO) if you are unhappy with how we have handled your personal data or your rights request.</p>

  <!-- 11. Cookies -->
  <h2>11. Cookies</h2>
  <p>Our website uses cookies to distinguish you from other users of our website. This helps us to provide you with a good experience when you browse our website and also allows us to improve our site. For detailed information on the cookies we use, the purposes for which we use them, and how to manage your cookie preferences, please see our <strong>Cookie Policy</strong>.</p>

  <!-- 12. Changes -->
  <h2>12. Changes to This Policy</h2>
  <p>We may update this Privacy Policy from time to time. The most current version will always be available on our website and will apply from the date of publication. Any significant changes will be communicated to you via email or a notice on our website.</p>


</div>

"""
    },
    {
         'title' : 'Terms & Conditions',
            'slug' : 'terms-and-conditions',
            'intro' : "These Terms govern your use of our website, event registrations, and the professional event management services we provide.",
            'body' : """
                    <div class="container">

  <h1>Terms &amp; Conditions · NME Music</h1>
  <p style="color: #475569; margin-top: -0.8rem; font-weight: 500;">
    <span class="badge">Last Updated</span>
    <strong>20 July 2026</strong>
  </p>

  <!-- 1. Introduction -->
  <h2>1. Introduction</h2>
  <p>
    Welcome to NME Music. These Terms and Conditions ("Terms") govern your use of our website, our event hosting and management services, and any events we organise or manage on behalf of clients.
    By accessing our website, registering for an event, or engaging our services, you agree to be bound by these Terms.
  </p>
  <p>
    Please read these Terms carefully before using our services. If you do not agree with any part of these Terms, you must not use our website or services.
  </p>

  <div class="highlight-box">
    <p><strong>📌 Quick Summary:</strong> These Terms cover your use of our website, event registrations, ticket purchases, service agreements, and your rights and obligations when engaging with NME Music.</p>
  </div>

  <!-- 2. Definitions -->
  <h2>2. Definitions</h2>
  <p>In these Terms, the following words have the following meanings:</p>
  <ul>
    <li><strong>"NME Music"</strong>, <strong>"we"</strong>, <strong>"us"</strong>, or <strong>"our"</strong> refers to NME Music, a UK-based event hosting and management company.</li>
    <li><strong>"You"</strong> or <strong>"your"</strong> refers to the user, attendee, client, or visitor to our website.</li>
    <li><strong>"Services"</strong> refers to all event hosting, event management, production, and related services offered by NME Music.</li>
    <li><strong>"Event"</strong> refers to any show, festival, conference, corporate gathering, private function, or other occasion hosted or managed by NME Music.</li>
    <li><strong>"Website"</strong> refers to www.nmemusic.co.uk and all associated subdomains.</li>
    <li><strong>"Ticket"</strong> refers to any ticket, pass, or entry credential purchased or issued for an Event.</li>
    <li><strong>"Client"</strong> refers to any individual or organisation that contracts NME Music to provide event management services.</li>
  </ul>

  <!-- 3. Our Services -->
  <h2>3. Our Services</h2>
  <p>NME Music provides the following services:</p>
  <ul>
    <li><strong>Event Hosting:</strong> We organise and host our own events, including concerts, festivals, and showcases.</li>
    <li><strong>Event Management:</strong> We provide professional event management services to clients, including planning, production, logistics, and on-the-day coordination.</li>
    <li><strong>Consultancy:</strong> We offer strategic advice and support for event planning and execution.</li>
  </ul>
  <p>
    All services are provided subject to these Terms and any additional terms agreed in writing between NME Music and the Client.
  </p>

  <!-- 4. Event Registration & Tickets -->
  <h2>4. Event Registration &amp; Tickets</h2>

  <h3>4.1 General</h3>
  <p>
    When you register for or purchase tickets to an Event hosted by NME Music, you agree to provide accurate and complete information.
    You are responsible for ensuring that all details provided are correct at the time of purchase.
  </p>

  <h3>4.2 Ticket Purchase</h3>
  <ul>
    <li>All ticket prices are displayed in GBP (£) and include applicable VAT unless otherwise stated.</li>
    <li>Payment must be made in full at the time of booking.</li>
    <li>We accept payment via the methods specified on our booking platform.</li>
    <li>Confirmation of your booking will be sent to the email address you provide.</li>
  </ul>

  <h3>4.3 Ticket Refunds &amp; Exchanges</h3>
  <ul>
    <li>All ticket sales are <strong>final</strong> and non-refundable unless otherwise stated at the time of purchase.</li>
    <li>In the event of a cancellation or rescheduling of an Event by NME Music, ticket holders will be offered a refund or the option to transfer their ticket to the rescheduled date.</li>
    <li>Refunds will be processed using the original payment method within 14 business days of the cancellation announcement.</li>
    <li>We are not responsible for any travel, accommodation, or other expenses incurred in connection with an Event.</li>
  </ul>

  <h3>4.4 Event Cancellation by Attendee</h3>
  <p>
    If you are unable to attend an Event for any reason, you may transfer your ticket to another person, provided you notify us in writing at least 48 hours before the Event.
    Name changes may be subject to an administrative fee.
  </p>

  <h3>4.5 Age Restrictions</h3>
  <p>
    Certain Events may have age restrictions, which will be clearly stated on the Event page.
    It is your responsibility to ensure you meet the age requirements for the Event you are booking.
    We reserve the right to refuse entry or cancel tickets without refund if age restrictions are not met.
  </p>

  <!-- 5. Client Services -->
  <h2>5. Client Services</h2>

  <h3>5.1 Engagement</h3>
  <p>
    Clients engaging NME Music for event management services must enter into a separate written agreement ("Service Agreement").
    These Terms apply in addition to any terms set out in the Service Agreement.
    In the event of any conflict, the Service Agreement shall prevail.
  </p>

  <h3>5.2 Client Obligations</h3>
  <ul>
    <li>You agree to provide all necessary information, access, and cooperation to enable us to deliver the Services effectively.</li>
    <li>You are responsible for obtaining any necessary permits, licences, or permissions required for your Event, unless otherwise agreed in writing.</li>
    <li>You agree to pay all fees and expenses as outlined in the Service Agreement.</li>
  </ul>

  <h3>5.3 Cancellation by Client</h3>
  <p>
    If you wish to cancel a Service Agreement, you must notify us in writing.
    Cancellation charges will apply as set out in the Service Agreement.
  </p>

  <!-- 6. Intellectual Property -->
  <h2>6. Intellectual Property</h2>
  <p>
    All content on our Website, including text, images, logos, graphics, designs, and software, is the property of NME Music or its licensors and is protected by UK and international copyright and intellectual property laws.
  </p>
  <p>
    You may not reproduce, distribute, modify, or exploit any content from our Website without our prior written consent.
  </p>
  <p>
    Any intellectual property created by NME Music in the course of providing Services (including event concepts, branding, and content) shall remain our property unless otherwise agreed in writing.
  </p>

  <!-- 7. User Conduct -->
  <h2>7. User Conduct</h2>
  <p>When using our Website or attending our Events, you agree not to:</p>
  <ul>
    <li>Engage in any unlawful, fraudulent, or harmful activity.</li>
    <li>Disrupt or interfere with the operation of our Website or Events.</li>
    <li>Use our Website or Services to harass, abuse, or harm others.</li>
    <li>Impersonate any person or entity or misrepresent your affiliation with us.</li>
    <li>Attempt to gain unauthorised access to our systems or networks.</li>
  </ul>
  <p>
    We reserve the right to refuse entry to any Event or terminate access to our Website if we reasonably believe you have breached these Terms.
  </p>

  <!-- 8. Photography & Videography -->
  <h2>8. Photography &amp; Videography</h2>
  <p>
    By attending an Event hosted or managed by NME Music, you consent to being photographed and/or filmed.
    These images and recordings may be used for promotional purposes, including on our website, social media, and marketing materials.
  </p>
  <p>
    If you do not wish to be photographed or filmed, please notify a member of our team at the Event or contact us in advance at <a href="mailto:info@nmemusic.co.uk">info@nmemusic.co.uk</a>.
    We will make reasonable efforts to accommodate your request but cannot guarantee that you will not appear in any recordings.
  </p>

  <!-- 9. Health & Safety -->
  <h2>9. Health &amp; Safety</h2>
  <p>
    The safety and well-being of our attendees, clients, and staff are of paramount importance.
    By attending an Event, you agree to:
  </p>
  <ul>
    <li>Follow all health and safety instructions provided by NME Music staff or venue personnel.</li>
    <li>Comply with any venue rules and regulations.</li>
    <li>Notify a member of staff of any hazards or incidents immediately.</li>
    <li>Take reasonable care for your own health and safety and that of others.</li>
  </ul>
  <p>
    We reserve the right to refuse entry or remove any individual who poses a risk to the safety of others.
  </p>

  <!-- 10. Limitation of Liability -->
  <h2>10. Limitation of Liability</h2>
  <p>
    To the fullest extent permitted by UK law, NME Music shall not be liable for:
  </p>
  <ul>
    <li>Any indirect, incidental, or consequential loss or damage.</li>
    <li>Any loss of profits, revenue, data, or goodwill.</li>
    <li>Any loss or damage arising from your use of our Website or Services.</li>
    <li>Any loss or damage caused by events beyond our reasonable control (including but not limited to acts of God, strikes, civil unrest, pandemics, or government restrictions).</li>
  </ul>
  <p>
    Our total liability to you in connection with these Terms shall not exceed the total amount paid by you to us for the relevant Service or Ticket, or £500, whichever is higher.
  </p>
  <p>
    Nothing in these Terms limits or excludes our liability for death or personal injury caused by our negligence, fraud, or any other liability that cannot be excluded by UK law.
  </p>

  <!-- 11. Indemnity -->
  <h2>11. Indemnity</h2>
  <p>
    You agree to indemnify and hold NME Music, its directors, employees, and agents harmless from and against any claims, losses, damages, liabilities, costs, and expenses (including legal fees) arising from:
  </p>
  <ul>
    <li>Your breach of these Terms.</li>
    <li>Your use of our Website or Services.</li>
    <li>Your violation of any law or the rights of any third party.</li>
    <li>Your attendance at any Event.</li>
  </ul>

  <!-- 12. Third-Party Links -->
  <h2>12. Third-Party Links</h2>
  <p>
    Our Website may contain links to third-party websites or services that are not owned or controlled by NME Music.
    We have no control over, and assume no responsibility for, the content, privacy policies, or practices of any third-party websites.
    You access such websites at your own risk.
  </p>

  <!-- 13. Data Protection -->
  <h2>13. Data Protection</h2>
  <p>
    We take your privacy seriously.
    Any personal data we collect will be processed in accordance with our <a href="privacy-policy.html">Privacy Policy</a> and applicable data protection laws, including the UK GDPR and the Data Protection Act 2018.
  </p>
  <p>
    By using our Services, you consent to our collection and use of your personal data as described in our Privacy Policy.
  </p>

  <!-- 14. Governing Law & Jurisdiction -->
  <h2>14. Governing Law &amp; Jurisdiction</h2>
  <p>
    These Terms shall be governed by and construed in accordance with the laws of England and Wales.
  </p>
  <p>
    Any disputes arising out of or in connection with these Terms shall be subject to the exclusive jurisdiction of the courts of England and Wales.
  </p>

  <!-- 15. Amendments -->
  <h2>15. Amendments</h2>
  <p>
    We reserve the right to amend these Terms at any time.
    Any changes will be effective immediately upon posting on our Website.
    It is your responsibility to review these Terms periodically for any updates.
    Your continued use of our Website or Services after any changes constitutes your acceptance of the revised Terms.
  </p>

  <!-- 16. Severability -->
  <h2>16. Severability</h2>
  <p>
    If any provision of these Terms is found to be invalid, illegal, or unenforceable by a court of competent jurisdiction, the remaining provisions shall remain in full force and effect.
  </p>

  <!-- 17. Waiver -->
  <h2>17. Waiver</h2>
  <p>
    Our failure to enforce any right or provision of these Terms shall not be deemed a waiver of such right or provision.
    Any waiver must be in writing and signed by an authorised representative of NME Music.
  </p>

  <!-- 18. Entire Agreement -->
  <h2>18. Entire Agreement</h2>
  <p>
    These Terms, together with our <a href="privacy-policy.html">Privacy Policy</a> and <a href="cookie-policy.html">Cookie Policy</a>, constitute the entire agreement between you and NME Music regarding your use of our Website and Services.
    They supersede all prior or contemporaneous communications and proposals, whether oral or written.
  </p>

  <!-- 19. Contact Us -->
  <h2>19. Contact Us</h2>
  <p>
    If you have any questions, concerns, or requests regarding these Terms, please contact us using the details below.
  </p>

  <div class="contact-block">
    <p><strong>NME Music</strong></p>
    <p>Email: <a href="mailto:info@nmemusic.co.uk">info@nmemusic.co.uk</a></p>
    <p>Address: [Insert your registered business address]</p>
  </div>



</div>
        """
    },
    {
        'title' : 'Cookie Policy',
        'slug' : 'cookie-policy',
        'intro' : "We use only essential functional cookies to keep our website working properly — no tracking, no analytics, no marketing.",
        'body' : """
   
            <div class="container">

        <h1>Cookie Policy · NME Music</h1>
        <p style="color: #475569; margin-top: -0.8rem; font-weight: 500;">
        <span class="badge">UK GDPR compliant</span>
        Last Updated: <strong>20 July 2026</strong>
        </p>

        <!-- 1. Introduction -->
        <h2>1. Introduction</h2>
        <p>
        NME Music (&ldquo;we&rdquo;, &ldquo;us&rdquo;, or &ldquo;our&rdquo;) is committed to protecting your privacy and being transparent about how we use cookies on our website.
        This Cookie Policy explains what cookies are, how we use them, and your choices regarding their use.
        </p>
        <p>
        This policy applies to all visitors to our website at <strong>www.nmemusic.co.uk</strong> (the &ldquo;Site&rdquo;).
        It should be read alongside our <a href="privacy-policy.html">Privacy Policy</a>.
        </p>

        <div class="highlight-box">
        <p><strong>🔒 Our Promise:</strong> We only use <strong>functional cookies</strong> that are strictly necessary for the operation of our website. We do <strong>not</strong> use any analytics, tracking, advertising, or third-party marketing cookies.</p>
        </div>

        <!-- 2. What Are Cookies -->
        <h2>2. What Are Cookies?</h2>
        <p>
        Cookies are small text files that are placed on your device (computer, tablet, or mobile phone) when you visit a website.
        They are widely used to make websites work more efficiently and to provide information to the site owners.
        </p>
        <p>
        Cookies are <strong>not</strong> viruses, spyware, or malware. They cannot access your hard drive or collect any personal information without your explicit consent.
        </p>

        <!-- 3. How We Use Cookies -->
        <h2>3. How We Use Cookies</h2>
        <p>
        At NME Music, we use cookies <strong>only for functional purposes</strong>. These cookies are essential to enable you to navigate our Site and use its core features.
        </p>
        <p>Specifically, we use functional cookies to:</p>
        <ul>
        <li>Remember your cookie consent preference (so we don&rsquo;t show you the cookie banner repeatedly).</li>
        <li>Maintain your session if you are logged in to a client portal or account area.</li>
        <li>Enable essential site functionality such as form submissions and navigation.</li>
        <li>Maintain security and prevent fraudulent activity.</li>
        </ul>
        <p>
        These cookies do not collect any personal data that could be used for marketing or profiling purposes.
        They are automatically deleted when you close your browser (session cookies) or may persist for a short period to remember your preferences (persistent cookies).
        </p>

        <!-- 4. List of Cookies -->
        <h2>4. The Cookies We Use</h2>
        <p>
        Since we only use functional cookies, the list below is intentionally short and transparent.
        </p>

        <table>
        <thead>
            <tr>
            <th>Cookie Name</th>
            <th>Purpose</th>
            <th>Duration</th>
            <th>Type</th>
            </tr>
        </thead>
        <tbody>
            <tr>
            <td><code>cookie_consent</code></td>
            <td>Stores your cookie preference so we don&rsquo;t show the cookie banner again.</td>
            <td>365 days (persistent)</td>
            <td>Functional / Strictly Necessary</td>
            </tr>
            <tr>
            <td><code>session_id</code></td>
            <td>Maintains your browsing session for essential site functionality.</td>
            <td>Session (expires when you close your browser)</td>
            <td>Functional / Strictly Necessary</td>
            </tr>
            <tr>
            <td><code>csrf_token</code></td>
            <td>Helps protect against cross-site request forgery (security).</td>
            <td>Session (expires when you close your browser)</td>
            <td>Functional / Strictly Necessary</td>
            </tr>
        </tbody>
        </table>

        <p>
        <strong>Note:</strong> We do <strong>not</strong> use any third-party cookies, analytics cookies (such as Google Analytics), marketing cookies, or tracking cookies of any kind.
        </p>

        <!-- 5. Your Consent -->
        <h2>5. Your Consent and Choices</h2>
        <p>
        When you first visit our website, we display a cookie banner requesting your consent to use functional cookies.
        By clicking &ldquo;Accept &amp; Close,&rdquo; you agree to our use of these essential cookies.
        </p>
        <p>
        Under the UK GDPR and the Privacy and Electronic Communications Regulations (PECR), we are permitted to place strictly necessary cookies without your explicit consent.
        However, we choose to be transparent and provide you with clear information about our use of cookies.
        </p>

        <h3>How to manage cookies in your browser</h3>
        <p>
        Most web browsers allow you to control cookies through your browser settings.
        You can choose to block or delete cookies at any time.
        However, please note that if you block functional cookies, some parts of our Site may not work properly.
        </p>
        <p>Below are links to the cookie management pages for the most common browsers:</p>
        <ul>
        <li><a href="https://support.google.com/chrome/answer/95647" target="_blank" rel="noopener">Google Chrome</a></li>
        <li><a href="https://support.mozilla.org/en-US/kb/enable-and-disable-cookies-website-preferences" target="_blank" rel="noopener">Mozilla Firefox</a></li>
        <li><a href="https://support.apple.com/en-gb/guide/safari/sfri11471/mac" target="_blank" rel="noopener">Safari</a></li>
        <li><a href="https://support.microsoft.com/en-us/microsoft-edge/delete-cookies-in-microsoft-edge-63947406-40ac-c3b8-57b9-2a946a29ae09" target="_blank" rel="noopener">Microsoft Edge</a></li>
        </ul>

        <!-- 6. Contact -->
        <h2>6. Contact Us</h2>
        <p>
        If you have any questions about our use of cookies, or if you would like further information, please do not hesitate to contact us.
        </p>

        <div class="contact-block">
        <p><strong>NME Music</strong></p>
        <p>Email: <a href="mailto:info@nmemusic.co.uk">info@nmemusic.co.uk</a></p>
        <p>Address: [Insert your registered business address]</p>
        </div>

        <!-- 7. Changes -->
        <h2>7. Changes to This Policy</h2>
        <p>
        We may update this Cookie Policy from time to time to reflect changes in technology, regulation, or our business practices.
        The most current version will always be available on our website.
        Any significant changes will be communicated via a notice on our Site or by email.
        </p>
        <p>
        This policy was last updated on <strong>20 July 2026</strong>.
        </p>


  </div>
            """
    }
]

def seed_app():
    
    for page in page_data:
        new_page = Page(
            title = page['title'],
            description = page['description'],
            keywords = page['keywords'],
            tag = page['tag'],   
        )

        db.session.add(new_page)
    db.session.flush()
    
    for section in section_data:
        new_section = Section(
            page_id = section.get('page_id'),
            title = section.get('title'),
            subtitle = section.get('subtitle'),
            text = section.get('text'),
            tag = section.get('tag')
        )
        db.session.add(new_section)

    generes_to_add = []
    for g in genre_data:
        new_genre = Genre(
            **g
        )
        generes_to_add.append(new_genre)
        
        db.session.add(new_genre)

    db.session.flush()

    for service in service_data:
        new_service = Service(
            **service
        )
        db.session.add(new_service)

    for event in event_data:
        new_event = Event(**event)
        new_event.slug = slugify(event['title'])
        new_event.genres.append(generes_to_add[0])
        print(new_event.slug)
        db.session.add(new_event)

    for policy in policy_data:
        new_policy = Policy(**policy)
        db.session.add(new_policy)

    db.session.commit()

if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        seed_app()