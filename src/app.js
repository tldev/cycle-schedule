document.addEventListener('DOMContentLoaded', async () => {
    try {
        // --- ⚙️ DRUG INFORMATION DATABASE ⚙️ ---
        const drugInfo = {
            "Prenatal Vitamins": { color: "var(--color-prenatal)", icon: "💊" },
            "Omnitrope": { color: "var(--color-omnitrope)", icon: "💉", videoUrl: "https://www.youtube.com/watch?v=NS0ca3T7wRM" },
            "Norethindrone": { color: "var(--color-norethindrone)", icon: "💊" },
            "Estradiol": { color: "var(--color-estradiol)", icon: "💊" },
            "Clomid": { color: "var(--color-clomid)", icon: "💊" },
            "Follistim": { color: "var(--color-follistim)", icon: "💉", videoUrl: "https://www.youtube.com/watch?v=0iz5zu13Gnk" },
            "Menopur": { color: "var(--color-menopur)", icon: "💉", videoUrl: "https://www.youtube.com/watch?v=HBrRpb436A0" },
            "Ganirelix": { color: "var(--color-ganirelix)", icon: "💉", videoUrl: "https://www.youtube.com/watch?v=m1pDSK-1pHM" },
            "Pregnyl": { color: "var(--color-pregnyl)", icon: "💉", videoUrl: "https://www.youtube.com/watch?v=seXGpX_uFBg" },
        };

        // --- 🗓️ Fetch Schedule Data 🗓️ ---
        const response = await fetch('schedule.json');
        if (!response.ok) {
            throw new Error(`Failed to load schedule: ${response.statusText}`);
        }
        const schedule = await response.json();

        // --- 💡 APPLICATION LOGIC 💡 ---
        let currentCalendarDate = new Date();
        let selectedDayElement = null;

        const getEl = (id) => document.getElementById(id);

        const views = {
            today: getEl('today-view'),
            calendar: getEl('calendar-view'),
            legend: getEl('legend-view')
        };
        const buttons = {
            today: getEl('today-btn'),
            calendar: getEl('calendar-btn'),
            legend: getEl('legend-btn')
        };
        const calendarDetailsView = getEl('calendar-day-details');

        const formatDate = (date, options) => new Date(date + 'T12:00:00').toLocaleDateString('en-US', options);

        const generateDayContent = (dayData) => {
            if (!dayData || (!dayData.milestone && !dayData.appointments?.length && !dayData.medications?.length)) {
                return '<div class="card"><p>No scheduled items for this day.</p></div>';
            }

            let html = '';
            if (dayData.milestone) {
                html += `<div class="card"><h3>Milestone</h3><p>${dayData.milestone}</p></div>`;
            }
            if (dayData.appointments?.length) {
                html += `<div class="card"><h3>Appointments</h3><ul>`;
                dayData.appointments.forEach(appt => {
                    html += `<li class="med-item"><span class="med-icon">📅</span><div class="med-info"><div class="med-name">${appt.time}: ${appt.what}</div><div class="med-details">${appt.where}</div></div></li>`;
                });
                html += `</ul></div>`;
            }
            if (dayData.medications?.length) {
                html += `<div class="card"><h3>Medications</h3><ul>`;
                dayData.medications.forEach(med => {
                    const info = drugInfo[med.name] || { color: '#ccc', icon: '❓' };
                    const classes = ['med-item'];
                    if (med.is_start) classes.push('is-start');
                    if (med.is_stop) classes.push('is-stop');
                    if (med.is_trigger) classes.push('is-trigger');

                    let videoLinkHtml = '';
                    if (info.videoUrl) {
                        videoLinkHtml = `<a href="${info.videoUrl}" class="video-link" target="_blank" rel="noopener noreferrer" title="Watch instruction video">▶️</a>`;
                    }

                    html += `<li class="${classes.join(' ')}" style="border-left-color: ${info.color};">
                        <span class="med-icon">${info.icon}</span>
                        <div class="med-info">
                            <div class="med-name">${med.name}</div>
                            <div class="med-details">${med.details}</div>
                        </div>
                        ${videoLinkHtml}
                    </li>`;
                });
                html += `</ul></div>`;
            }
            return html;
        };

        const renderCalendarDayDetails = (dateString) => {
            const dayData = schedule.find(d => d.date === dateString);
            const header = `<h3 class="today-date">${formatDate(dateString, { weekday: 'long', month: 'long', day: 'numeric' })}</h3>`;
            const content = generateDayContent(dayData);
            calendarDetailsView.innerHTML = header + content;
        };

        const clearCalendarSelection = () => {
            if (selectedDayElement) {
                selectedDayElement.classList.remove('selected');
                selectedDayElement = null;
            }
            calendarDetailsView.innerHTML = '<p class="details-placeholder">Click a day with events to see details.</p>';
        };

        const handleDaySelection = (dayEl) => {
            if (selectedDayElement && selectedDayElement !== dayEl) {
                selectedDayElement.classList.remove('selected');
            }

            if (!dayEl || !dayEl.classList.contains('has-events')) {
                clearCalendarSelection();
                if (dayEl) {
                    renderCalendarDayDetails(dayEl.dataset.date);
                }
                return;
            }

            if (selectedDayElement === dayEl) {
                clearCalendarSelection();
                return;
            }

            dayEl.classList.add('selected');
            selectedDayElement = dayEl;
            renderCalendarDayDetails(dayEl.dataset.date);
        };

        const renderTodayView = () => {
            const today = new Date();
            const todayString = today.toLocaleDateString('sv-SE');
            const todayData = schedule.find(day => day.date === todayString);
            getEl('today-date').textContent = formatDate(todayString, { weekday: 'long', month: 'long', day: 'numeric' });
            getEl('today-content').innerHTML = generateDayContent(todayData);

            const tomorrow = new Date(today);
            tomorrow.setDate(tomorrow.getDate() + 1);
            const tomorrowString = tomorrow.toLocaleDateString('sv-SE');
            const tomorrowData = schedule.find(day => day.date === tomorrowString);

            const tomorrowPreviewEl = getEl('tomorrow-preview');
            tomorrowPreviewEl.innerHTML = `
                <h3 class="tomorrow-header">Tomorrow — ${formatDate(tomorrowString, { weekday: 'long', month: 'long', day: 'numeric' })}</h3>
                ${generateDayContent(tomorrowData)}
            `;
        };

        const renderCalendarView = () => {
            const calendarGrid = getEl('calendar-grid');
            calendarGrid.innerHTML = '';
            const year = currentCalendarDate.getFullYear();
            const month = currentCalendarDate.getMonth();
            const todayString = new Date().toLocaleDateString('sv-SE');

            getEl('calendar-month-year').textContent = currentCalendarDate.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });

            ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].forEach(day => {
                calendarGrid.innerHTML += `<div class="day-header">${day}</div>`;
            });

            const firstDayOfMonth = new Date(year, month, 1).getDay();
            const daysInMonth = new Date(year, month + 1, 0).getDate();

            for (let i = 0; i < firstDayOfMonth; i++) {
                calendarGrid.innerHTML += `<div class="day other-month"></div>`;
            }

            for (let i = 1; i <= daysInMonth; i++) {
                const dayString = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
                const dayData = schedule.find(d => d.date === dayString);
                const dayEl = document.createElement('div');
                dayEl.classList.add('day');
                dayEl.dataset.date = dayString;
                dayEl.innerHTML = `<span class="day-number">${i}</span>`;

                if (todayString === dayString) dayEl.classList.add('today');

                if (dayData && (dayData.medications?.length || dayData.appointments?.length || dayData.milestone)) {
                    dayEl.classList.add('has-events');
                    dayEl.setAttribute('role', 'button');
                    dayEl.setAttribute('tabindex', '0');

                    const icons = new Set();
                    if (dayData.appointments?.length) icons.add('📅');
                    dayData.medications?.forEach(med => icons.add(drugInfo[med.name]?.icon || '💊'));

                    const iconsContainer = document.createElement('div');
                    iconsContainer.className = 'day-icons';
                    iconsContainer.innerHTML = Array.from(icons).join('');
                    dayEl.appendChild(iconsContainer);
                }
                calendarGrid.appendChild(dayEl);
            }
        };

        const renderLegendView = () => {
            const legendList = getEl('legend-list');
            legendList.innerHTML = '';
            for (const [name, info] of Object.entries(drugInfo)) {
                const li = document.createElement('li');
                li.className = 'legend-item';

                const swatch = document.createElement('div');
                swatch.className = 'legend-color-swatch';
                swatch.style.backgroundColor = info.color;

                li.appendChild(swatch);

                let nameEl;
                if (info.videoUrl) {
                    nameEl = document.createElement('a');
                    nameEl.href = info.videoUrl;
                    nameEl.textContent = `${name} ↗`;
                    nameEl.target = '_blank';
                    nameEl.rel = 'noopener noreferrer';
                } else {
                    nameEl = document.createElement('span');
                    nameEl.textContent = name;
                }
                li.appendChild(nameEl);

                legendList.appendChild(li);
            }
        };

        const switchView = (viewName) => {
            Object.values(views).forEach(v => v.classList.add('hidden'));
            Object.values(buttons).forEach(b => b.classList.remove('active'));
            views[viewName].classList.remove('hidden');
            buttons[viewName].classList.add('active');

            if (viewName !== 'calendar') {
                clearCalendarSelection();
            }
        };

        // Event Listeners
        Object.keys(buttons).forEach(key => buttons[key].addEventListener('click', () => switchView(key)));

        getEl('go-to-today-btn').addEventListener('click', () => {
            currentCalendarDate = new Date();
            renderCalendarView();
            const todayElement = document.querySelector('.day.today');
            handleDaySelection(todayElement);
        });

        getEl('prev-month-btn').addEventListener('click', () => {
            currentCalendarDate.setMonth(currentCalendarDate.getMonth() - 1);
            renderCalendarView();
            clearCalendarSelection();
        });

        getEl('next-month-btn').addEventListener('click', () => {
            currentCalendarDate.setMonth(currentCalendarDate.getMonth() + 1);
            renderCalendarView();
            clearCalendarSelection();
        });

        getEl('calendar-grid').addEventListener('click', (e) => {
            handleDaySelection(e.target.closest('.day.has-events'));
        });

        getEl('calendar-grid').addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                handleDaySelection(e.target.closest('.day.has-events'));
            }
        });

        // Initial Load
        renderTodayView();
        renderCalendarView();
        renderLegendView();

    } catch (error) {
        console.error("Application Error:", error);
        document.querySelector('main').innerHTML = `
            <div class="card" style="background-color: #fff0f1; border-color: var(--trigger-color);">
                <h3>An Error Occurred</h3>
                <p>Could not load the application. Please check the console for details or try again later.</p>
                <p><strong>Error:</strong> ${error.message}</p>
            </div>
        `;
    }
});