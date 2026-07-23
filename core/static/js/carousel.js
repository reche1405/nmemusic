 // ---------- CONFIGURATION ----------
        let AUTO_INTERVAL_MS = 1500;      // autoplay display time
        const TRANSITION_MS = 500;           // scroll animation duration (matches CSS transition)
        const DESKTOP_VISIBLE = 3;
        const TABLET_VISIBLE = 2;
        const MOBILE_VISIBLE = 1;
        
        // ---------- GLOBALS ----------
        let slidesData = [];          // stores original slide objects {id, title, icon, desc}
        let totalRealSlides = 0;      
        let virtualSlides = [];       // array after infinite duplication (left/right clones)
        let currentIndex = 0;         // index inside virtualSlides that points to "first visible slide" logical position
        let visibleCount = DESKTOP_VISIBLE;
        let trackEl = document.getElementById('track');
        let viewportEl = document.getElementById('viewport');
        let prevBtn = document.getElementById('prevBtn');
        let nextBtn = document.getElementById('nextBtn');
        let playPauseBtn = document.getElementById('playPauseBtn');
        let indicatorsContainer = document.getElementById('indicators');
        
        let autoPlayInterval = null;
        let isPlaying = true;
        let isTransitioning = false;        // lock while animating to prevent multiple triggers
        let resizeObserver = null;
        
        // swipe variables
        let touchStartX = 0;
        let touchMoveX = 0;
        let isSwiping = false;
        let swipeThreshold = 50;


        try {
        // If carouselData exists globally, use it. Otherwise, look for it.
        let dataSrc = typeof carouselData !== 'undefined' ? carouselData : null;

        if (!dataSrc) {
            // Fallback: Attempt to grab it if it was inside a script tag directly
            const scriptEl = document.getElementById('carousel-data-script');
            if (scriptEl) {
                // Evaluates the string script safely if it was injected
                eval(scriptEl.innerHTML);
                if (typeof carouselData !== 'undefined') {
                    dataSrc = carouselData;
                }
            }
        }

        if (dataSrc && dataSrc.items) {
            // Extract dynamically supplied autoplay interval if it exists
            if (dataSrc.autoplay_interval) {
                AUTO_INTERVAL_MS = dataSrc.autoplay_interval;
            }

            // Map your actual items into slidesData
            dataSrc.items.forEach(item => {
                slidesData.push({
                    id: item.id,
                    icon: item.url, // Using 'url' here instead of an emoji icon
                    title: item.title,
                    desc: item.description || item.desc || ''
                });
            });
        }
    } catch (e) {
        console.error("Failed to parse carousel data script wrapper:", e);
    }
        if (slidesData.length < 1) {

            const sampleIcons = ["🎨", "🚀", "🎵", "📸", "⚡", "🍕", "🏔️", "🎮", "💡", "🌈"];
            const sampleTitles = ["Creativity", "Velocity", "Melody", "Snapshot", "Energy", "Fusion", "Horizon", "Arcade", "Insight", "Prism"];
            const sampleDescs = ["Infinite ideas", "Fast & smooth", "Harmonic sound", "Capture moment", "Power boost", "Tasty treats", "Wild peaks", "Play quest", "Bright minds", "Color burst"];
            
            for (let i = 0; i < 12; i++) {   // 12 original cards gives nice loop feel
                let icon = sampleIcons[i % sampleIcons.length];
                let title = `${sampleTitles[i % sampleTitles.length]} ${i+1}`;
                let desc = sampleDescs[i % sampleDescs.length];
                slidesData.push({ id: i, icon: icon, title: title, desc: desc });
            }
        }
        // ---------- GENERATE SAMPLE SLIDES (10 distinct cards) ----------
        totalRealSlides = slidesData.length;
        
        // ---------- INFINITE LOOP: BUILD VIRTUAL ARRAY (duplicate left & right) ----------
        // We need at least visibleCount extra clones on each side for seamless infinite.
        // For safety we duplicate X times where X >= visibleCount (max visible across breakpoints = 5)
        const cloneFactor = 3;  // ensure enough clones for extreme edge cases (3 full sets)
        function buildVirtualArray() {
            let leftClones = [];
            let rightClones = [];
            // clone full cycles from end to start for left side
            for (let i = 0; i < cloneFactor; i++) {
                leftClones.push(...slidesData.slice().reverse()); // or simple cycle? better consistency: actual slides but reversed can cause odd order? 
                // For seamless infinite, we need original order clones. More robust: take whole slidesData arrays
            }
            // simpler approach: repeat slidesData many times to have large buffer and maintain order.
            // cleaner: generate virtual array = [cloneRightSegment] + original + [cloneLeftSegment] where clones represent beginning/end.
            // To keep ordering intuitive: we'll create 3 copies of original in sequence (original in middle).
            // but we want natural left/right transition: user never sees boundary.
            // let virtual = [ ...slidesData.slice(-visibleCount), ...slidesData, ...slidesData.slice(0, visibleCount) ];
            // using dynamic visibleCount max 5 -> 5 prefix and 5 suffix works but we must ensure transform jumps.
            // Modern approach: replicate full set multiple times. Starting index = originalStart offset.
            const repeats = 5;   // large enough to cover any drag/button
            let virtual = [];
            for (let i = 0; i < repeats; i++) {
                virtual.push(...slidesData);
            }
            // Set currentIndex to point to first element of the first "original" cluster
            // original cluster starts at index (repeats/2 * totalRealSlides) roughly.
            let startOffset = Math.floor(repeats / 2) * totalRealSlides;
            return { virtualArray: virtual, startIdx: startOffset };
        }
        
        let virtualArray = [];
        let virtualStartOffset = 0;
        
        function initVirtual() {
            const res = buildVirtualArray();
            virtualArray = res.virtualArray;
            virtualStartOffset = res.startIdx;
            currentIndex = virtualStartOffset;
            renderTrackSlides();
            updateIndicatorsFromRealIndex();
        }
        
        // Get real slide index (0..totalRealSlides-1) from virtual index
        function getRealIndexFromVirtual(virtualIdx) {
            if (virtualArray.length === 0) return 0;
            return virtualIdx % totalRealSlides;
        }
        
        // get current real index (based on first visible slide from currentIndex)
        function getCurrentRealIndex() {
            if (virtualArray.length === 0) return 0;
            let firstVisibleVirtual = currentIndex;
            return firstVisibleVirtual % totalRealSlides;
        }
        
        // update dot indicators
        function updateIndicatorsFromRealIndex() {
            const realIdx = getCurrentRealIndex();
            const dots = document.querySelectorAll('.dot');
            dots.forEach((dot, i) => {
                if (i === realIdx) dot.classList.add('active');
                else dot.classList.remove('active');
            });
        }
        
        // render slides to DOM based on virtualArray and current visible range
        function renderTrackSlides() {
            if (!trackEl) return;
            const totalVirtual = virtualArray.length;
            // we only render a subset for performance? but we render all virtual (it's manageable, max 5*12=60 items)
            // However to keep DOM clean, just render whole virtual array once and update transform.
            // But if we change slides only after data change, we can render full track.
            // Efficient: render once during init, then never re-render whole set unless data changes.
            // We'll render full track only once and just update transform.
            if (trackEl.children.length === 0 || trackEl.children.length !== virtualArray.length) {
                trackEl.innerHTML = '';
                virtualArray.forEach((slide, idx) => {
                    const slideDiv = document.createElement('div');
                    slideDiv.className = 'carousel-slide';
                    slideDiv.setAttribute('data-virtual-idx', idx);
                    const isImageUrl = slide.icon.startsWith('/') || slide.icon.startsWith('http');
                    const image = document.createElement('img');
                    image.src = slide.icon; 
                    image.classList.add('object-cover')
                    const card = document.createElement('div');
                    card.classList.add('card'); 
                    slideDiv.appendChild(card);

                    card.appendChild(image);
        
                    card.innerHTML += `
                
                            <div class="card-title">${escapeHtml(slide.title)}</div>
                            <div class="card-desc">${escapeHtml(slide.desc)}</div>
                    `;
                    trackEl.appendChild(slideDiv);
                });
            }
            // Update slides widths based on current visibleCount
            updateSlideWidths();
            // Apply transform to show correct offset
            applyTransform();
        }
        
        function escapeHtml(str) {
            return str.replace(/[&<>]/g, function(m) {
                if (m === '&') return '&amp;';
                if (m === '<') return '&lt;';
                if (m === '>') return '&gt;';
                return m;
            }).replace(/[\uD800-\uDBFF][\uDC00-\uDFFF]/g, function(c) {
                return c;
            });
        }
        
        // update per-slide width based on visibleCount and container width
        function updateSlideWidths() {
            const slides = trackEl.querySelectorAll('.carousel-slide');
            if (!slides.length) return;
            const percent = 100 / visibleCount;
            slides.forEach(slide => {
                slide.style.width = `${percent}%`;
            });
        }
        
        // compute transform offset to make currentIndex the first visible slide
        function getTransformOffset() {
            const slideElements = trackEl.querySelectorAll('.carousel-slide');
            if (!slideElements.length) return 0;
            // each slide width (including padding? but width uses flex basis, we need actual offset in pixels)
            const firstSlide = slideElements[0];
            const slideRect = firstSlide.getBoundingClientRect();
            const slideFullWidth = slideRect.width;
            // offset = currentIndex * slide width
            return -(currentIndex * slideFullWidth);
        }
        
        function applyTransform() {
            if (!trackEl || isTransitioning === 'jump') return;
            const offset = getTransformOffset();
            trackEl.style.transform = `translate3d(${offset}px, 0, 0)`;
        }
        
        // seamless infinite correction: after transition ends, check boundary and jump if needed
        function handleInfiniteCorrection() {
            const totalVirt = virtualArray.length;
            const thresholdBuffer = visibleCount; // number of visible slides
            
            // If currentIndex is too close to left edge (less than visibleCount)
            if (currentIndex < thresholdBuffer) {
                // jump forward by one full cycle of original slides
                const jumpAmount = totalRealSlides;
                let newIndex = currentIndex + jumpAmount;
                if (newIndex + visibleCount <= totalVirt) {
                    jumpWithoutTransition(newIndex);
                }
            }
            // If currentIndex is too close to right edge (beyond totalVirt - visibleCount - thresholdBuffer)
            else if (currentIndex + visibleCount + thresholdBuffer > totalVirt) {
                const jumpAmount = totalRealSlides;
                let newIndex = currentIndex - jumpAmount;
                if (newIndex >= 0) {
                    jumpWithoutTransition(newIndex);
                }
            }
            updateIndicatorsFromRealIndex();
        }
        
        function jumpWithoutTransition(newIndex) {
            if (!trackEl) return;
            isTransitioning = true;
            trackEl.style.transition = 'none';
            currentIndex = newIndex;
            const offset = getTransformOffset();
            trackEl.style.transform = `translate3d(${offset}px, 0, 0)`;
            // force reflow
            void trackEl.offsetHeight;
            trackEl.style.transition = `transform ${TRANSITION_MS}ms cubic-bezier(0.2, 0.9, 0.4, 1.1)`;
            isTransitioning = false;
            updateIndicatorsFromRealIndex();
        }
        
        function moveToSlide(deltaSteps) {
            if (isTransitioning) return;
            isTransitioning = true;
            const newIndex = currentIndex + deltaSteps;
            if (newIndex >= 0 && newIndex + visibleCount <= virtualArray.length) {
                currentIndex = newIndex;
                applyTransform();
                // after transition end, correct boundaries
                const onTransitionEnd = () => {
                    trackEl.removeEventListener('transitionend', onTransitionEnd);
                    isTransitioning = false;
                    handleInfiniteCorrection();
                    // reset play timer after manual interaction (reset autoplay cycle)
                    resetAutoPlayTimer();
                };
                trackEl.addEventListener('transitionend', onTransitionEnd, { once: true });
                // fallback timeout in case transitionend not fired
                setTimeout(() => {
                    if (isTransitioning === true) {
                        trackEl.dispatchEvent(new Event('transitionend'));
                    }
                }, TRANSITION_MS + 50);
            } else {
                // should not happen due to infinite prep, but fallback
                isTransitioning = false;
            }
            updateIndicatorsFromRealIndex();
        }
        
        function next() {
            if (isTransitioning) return;
            moveToSlide(1);
        }
        
        function prev() {
            if (isTransitioning) return;
            moveToSlide(-1);
        }
        
        // Autoplay
        function startAutoPlay() {
            if (autoPlayInterval) clearInterval(autoPlayInterval);
            autoPlayInterval = setInterval(() => {
                if (isPlaying && !isTransitioning) {
                    next();
                }
            }, AUTO_INTERVAL_MS);
        }
        
        function stopAutoPlay() {
            if (autoPlayInterval) {
                clearInterval(autoPlayInterval);
                autoPlayInterval = null;
            }
        }
        
        function resetAutoPlayTimer() {
            if (isPlaying) {
                stopAutoPlay();
                startAutoPlay();
            }
        }
        
        function togglePlayPause() {
            if (!playPauseBtn) return;
            isPlaying = !isPlaying;
            if (isPlaying) {
                startAutoPlay();
                playPauseBtn.innerHTML = '<span>⏸</span> Pause';
            } else {
                stopAutoPlay();
                playPauseBtn.innerHTML = '<span>▶</span> Play';
            }
        }
        
        // Swipe detection
        function onTouchStart(e) {
            if (isTransitioning) return;
            const touch = e.touches[0];
            touchStartX = touch.clientX;
            isSwiping = true;
            touchMoveX = 0;
            trackEl.style.cursor = 'grabbing';
        }
        
        function onTouchMove(e) {
            if (!isSwiping || isTransitioning) return;
            const currentX = e.touches[0].clientX;
            const deltaX = currentX - touchStartX;
            touchMoveX = deltaX;
            // optional: slight visual feedback, but we keep transform inertia? we don't partial drag in this version (clean)
        }
        
        function onTouchEnd(e) {
            if (!isSwiping || isTransitioning) {
                isSwiping = false;
                trackEl.style.cursor = 'grab';
                return;
            }
            const delta = touchMoveX;
            if (Math.abs(delta) > swipeThreshold) {
                if (delta > 0) {
                    prev();
                } else {
                    next();
                }
            }
            isSwiping = false;
            touchMoveX = 0;
            trackEl.style.cursor = 'grab';
            resetAutoPlayTimer();
        }
        
        // Responsive visible count detection
        function updateVisibleCount() {
            const width = window.innerWidth;
            if (width >= 1024) {
                visibleCount = DESKTOP_VISIBLE;
            } else if (width >= 640) {
                visibleCount = TABLET_VISIBLE;
            } else {
                visibleCount = MOBILE_VISIBLE;
            }
            updateSlideWidths();
            // After visibleCount changes, we must re-evaluate transform to correct position boundary.
            // Jump correction to keep current real slide in view as first visible slide.
            if (trackEl) {
                const oldIndex = currentIndex;
                // no need to change logic, but we reapply transform
                applyTransform();
                // correct boundaries if needed
                setTimeout(() => {
                    handleInfiniteCorrection();
                }, 10);
            }
            rebuildIndicators();
        }
        
        function rebuildIndicators() {
            if (!indicatorsContainer) return;
            indicatorsContainer.innerHTML = '';
            for (let i = 0; i < totalRealSlides; i++) {
                const dot = document.createElement('div');
                dot.classList.add('dot');
                if (i === getCurrentRealIndex()) dot.classList.add('active');
                dot.addEventListener('click', () => {
                    if (isTransitioning) return;
                    // map real slide i to virtual index: we need jump to a virtual index where real index = i and logical index around current cluster
                    const targetReal = i;
                    const currentReal = getCurrentRealIndex();
                    const deltaReal = (targetReal - currentReal + totalRealSlides) % totalRealSlides;
                    let steps = deltaReal;
                    if (steps > totalRealSlides/2) steps = steps - totalRealSlides;
                    if (steps !== 0) {
                        moveToSlide(steps);
                    }
                });
                indicatorsContainer.appendChild(dot);
            }
            updateIndicatorsFromRealIndex();
        }
        
        // initial render and event binding
        function init() {
            initVirtual();      // builds virtualArray & renders
            updateVisibleCount();
            rebuildIndicators();
            
            // attach events
            prevBtn.addEventListener('click', () => { if (!isTransitioning) prev(); resetAutoPlayTimer(); });
            nextBtn.addEventListener('click', () => { if (!isTransitioning) next(); resetAutoPlayTimer(); });
            if(playPauseBtn) {
                playPauseBtn.addEventListener('click', togglePlayPause);
            }
            
            // swipe
            viewportEl.addEventListener('touchstart', onTouchStart, { passive: false });
            viewportEl.addEventListener('touchmove', onTouchMove, { passive: false });
            viewportEl.addEventListener('touchend', onTouchEnd);
            viewportEl.addEventListener('mousedown', (e) => { if (e.button === 0) { /* optional mouse drag support for testing */ } });
            
            window.addEventListener('resize', () => {
                updateVisibleCount();
                applyTransform();
                handleInfiniteCorrection();
            });
            
            startAutoPlay();
        }
        
        // called after any DOM layout shift to maintain transform
        window.addEventListener('load', () => {
            init();
        });