

        // ----- ROTATING LIST OF WORDS (customizable) -----
        const WORDS_LIST = [
            "Festivals",
            "Events",
            "Music",
        ];
        
        // ----- animation timing configuration -----
        const LETTER_ANIMATION_DURATION_MS = 550;    // matches CSS duration 0.45s
        const DELAY_BETWEEN_LETTERS_MS = 70;         // sequential delay between each letter start (in ms)
        const WORD_VISIBLE_EXTRA_MS = 600;           // how long final word stays fully visible before fade-out / removal
        const FADE_OUT_WORD_MS = 600;                // brief fade-out transition before switching to next word
        const DELAY_BETWEEN_WORDS_MS = 100;          // small gap after fade out before building next word
        
        // runtime variables
        let currentWordIndex = 0;
        let animationTimeoutIds = [];      // store all timeouts to clear if needed
        let isAnimating = false;            // prevent overlapping cycles during forced reset
        let currentAnimationActive = false;  // to track if we are currently animating letters or word display
        let nextWordScheduled = false;
        let currentWordElement = document.getElementById("rotatingWordSpan");
        currentWordElement = null
        const statusDiv = document.getElementById("statusMessage");
        
        // Helper: clear all scheduled timeouts from the array
        function clearAllTimeouts() {
            for (let id of animationTimeoutIds) {
                clearTimeout(id);
            }
            animationTimeoutIds = [];
        }
        
        // Helper: stop any ongoing animation and clear word container
        function abortCurrentAnimation(resetState = true) {
            // cancel all pending timeouts to avoid race conditions
            clearAllTimeouts();
            isAnimating = false;
            currentAnimationActive = false;
            nextWordScheduled = false;
            if (resetState) {
                // optionally we do not reset index here; just stop visual
                if (currentWordElement) {
                    currentWordElement.innerHTML = "";   // clear all letter spans
                }
            }
        }
        
        // cleanup + reset the visual (used by restart or between words with safety)
        function resetWordDisplay() {
            if (currentWordElement) {
                currentWordElement.innerHTML = "";
            }
        }
        
        // Helper to update status message
        function setStatusMessage(msg, isError = false) {
            if (statusDiv) {
                statusDiv.textContent = msg;
                if (isError) {
                    statusDiv.style.color = "#ffaa88";
                    setTimeout(() => {
                        if (statusDiv) statusDiv.style.color = "#a0b5e6";
                    }, 1200);
                } else {
                    statusDiv.style.color = "#a0b5e6";
                }
            }
        }
        
        // core: animate a single word (spelling letter by letter with 3D flip)
        function animateWord(word, onCompleteCallback) {
            if (!currentWordElement) return;
            // abort any lingering animations before starting fresh word
            abortCurrentAnimation(false);
            resetWordDisplay();
            
            if (!word || word.length === 0) {
                if (onCompleteCallback) onCompleteCallback();
                return;
            }
            
            isAnimating = true;
            currentAnimationActive = true;
            setStatusMessage(`✨ spelling "${word}" letter by letter...`);
            
            const letters = word.split('');
            const letterSpans = [];
            
            // Create span elements for each letter, initially invisible (default opacity 0)
            // but we will apply inline animation-delay.
            for (let i = 0; i < letters.length; i++) {
                const letterChar = letters[i];
                const span = document.createElement('span');
                span.textContent = letterChar;
                // base styles are set from CSS: opacity:0, transform scale(0)
                // we add custom animation delay inline
                const delayMs = i * DELAY_BETWEEN_LETTERS_MS;
                span.style.animationDelay = `${delayMs}ms`;
                // optional: set display to inline-block (already via CSS)
                currentWordElement.appendChild(span);
                letterSpans.push(span);
            }
            
            // total animation time for last letter to finish flipping: lastLetterDelay + DURATION
            const lastLetterDelay = (letters.length - 1) * DELAY_BETWEEN_LETTERS_MS;
            const totalAnimationFinishTime = lastLetterDelay + LETTER_ANIMATION_DURATION_MS;
            
            // schedule: after all letters have finished their 3D flip animation, 
            // we keep the word visible for an extra WORD_VISIBLE_EXTRA_MS before fading/dismissing.
            const keepVisibleTimeout = setTimeout(() => {
                if (!currentAnimationActive) return;
                setStatusMessage(`✔️ "${word}" — fading out...`);
                
                // ADD THIS BLOCK - apply fade transition to all letters
                const allLetterSpans = document.querySelectorAll('#rotatingWordSpan span');
                const fadeDurationSec = (FADE_OUT_WORD_MS / 1000).toFixed(2);
                for (let span of allLetterSpans) {
                    span.style.opacity = '1';
                    span.style.transform = 'scale(1) rotateX(0)';
                    span.style.removeProperty('animation');
                    span.style.animation = 'none';
                    void span.offsetWidth;
                    span.style.transition = `opacity ${fadeDurationSec}s ease-out`;
                    void span.offsetWidth;

                    span.style.opacity = '0';
                }
                                
                const fadeTimeout = setTimeout(() => {
                    resetWordDisplay();
                    currentAnimationActive = false;
                    isAnimating = false;
                    if (onCompleteCallback) onCompleteCallback();
                }, FADE_OUT_WORD_MS);
                
                animationTimeoutIds.push(fadeTimeout);
            }, totalAnimationFinishTime + WORD_VISIBLE_EXTRA_MS);
            // Store timeouts to allow abort on reset
            animationTimeoutIds.push(keepVisibleTimeout);
            
            // Also store a "lastLetterTimeout" for potential status update? not necessary but add safety.
            // Additionally, for safety: prevent memory leaks, we push each letter delay timeouts not needed because they are just CSS,
            // but we also push a final safety wrapper for cancellation: Actually we need to keep track of the final completion chain.
            // Because keepVisibleTimeout is already in the array, that's enough.
        }
        
        // word rotation state machine
        let currentRotationActive = false;
        let rotationTimeoutId = null;
        
        // main function that starts showing the next word in the rotation sequence
        function showNextWord() {
            // if a reset or external abort wants to kill the rotation, we reset flags
            if (!currentRotationActive) return;
            
            // avoid re-entrant if we are still animating? we call this after the previous word fully completes.
            // but we also check if isAnimating flag prevents overlapping? But the previous word cleanup
            // sets isAnimating = false and triggers this via callback. So it's safe.
            if (isAnimating) {
                // safety: in case a glitch triggers while animating, delay call
                setTimeout(() => {
                    if (currentRotationActive && !isAnimating) showNextWord();
                }, 100);
                return;
            }
            
            // get current word from list
            const word = WORDS_LIST[currentWordIndex % WORDS_LIST.length];
            
            // update status and animate
            const onWordComplete = () => {
                // after word fully faded and cleaned, move to next index
                if (!currentRotationActive) return;
                currentWordIndex = (currentWordIndex + 1) % WORDS_LIST.length;
                // wait a small gap before starting the next word (clean transition)
                if (rotationTimeoutId) clearTimeout(rotationTimeoutId);
                rotationTimeoutId = setTimeout(() => {
                    if (currentRotationActive) {
                        showNextWord();
                    }
                }, DELAY_BETWEEN_WORDS_MS);
                animationTimeoutIds.push(rotationTimeoutId); // for reset clarity
            };
            
            animateWord(word, onWordComplete);
        }
        
        // start the full rotation cycle
        function startRotation() {
            if (currentRotationActive) {
                // already rotating, but we can "restart" from fresh index if needed
                stopRotation(false); // stop without resetting index?
            }
            // reset all flags and abort any ongoing animation
            abortCurrentAnimation(true);
            resetWordDisplay();
            currentRotationActive = true;
            currentWordIndex = 0;   // begin from first word (use fresh start)
            // clear any scheduled next-word call
            if (rotationTimeoutId) {
                clearTimeout(rotationTimeoutId);
                rotationTimeoutId = null;
            }
            setStatusMessage("🔄 starting word rotation...");
            // start first word
            showNextWord();
        }
        
        // stop rotation (optionally reset index) but preserves ability to restart
        function stopRotation(resetIndex = false) {
            currentRotationActive = false;
            if (rotationTimeoutId) {
                clearTimeout(rotationTimeoutId);
                rotationTimeoutId = null;
            }
            abortCurrentAnimation(true);
            if (resetIndex) {
                currentWordIndex = 0;
            }
            resetWordDisplay();
        }
        
        // restart sequence: fully cancel current animation, reset index and start fresh
        function restartSequence() {
            // kill all ongoing timers and animations
            if (currentRotationActive) {
                stopRotation(true);
            } else {
                abortCurrentAnimation(true);
                resetWordDisplay();
                currentWordIndex = 0;
            }
            // restart from fresh state
            currentRotationActive = true;
            setStatusMessage("⟳ restarting word cycle...");
            // little micro delay to avoid conflicts with any ghost callbacks
            setTimeout(() => {
                if (currentRotationActive) {
                    // ensure the container is empty
                    resetWordDisplay();
                    showNextWord();
                }
            }, 30);
        }
        
        // ----- initial setup and attaching reset button -----
        function init() {
            if (!currentWordElement) {
                console.error("Span element #rotatingWordSpan not found!");
                return;
            }
            // ensure empty initially
            resetWordDisplay();
            // start the rotation automatically
            startRotation();
            
            // attach reset button handler
            const resetBtn = document.getElementById("resetSequenceBtn");
            if (resetBtn) {
                resetBtn.addEventListener("click", (e) => {
                    e.preventDefault();
                    // user restart with fresh animation
                    restartSequence();
                });
            }
        }
        
        // expose optional for debugging, but not needed
        window.addEventListener("DOMContentLoaded", init);
    