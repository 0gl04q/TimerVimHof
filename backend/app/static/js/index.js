class WimHofTimer {
  constructor() {
    this.currentRound = 0;
    this.totalRounds = 3;
    this.isRunning = false;
    this.currentPhase = 'ready';
    this.timeRemaining = 0;

    // DOM elements
    this.timerDisplay = document.getElementById('timer');
    this.phaseDisplay = document.getElementById('currentPhase');
    this.roundDisplay = document.getElementById('roundCounter');
    this.resetBtn = document.getElementById('resetBtn');
    this.progressRing = document.querySelector('.progress-ring__circle');

    // Settings
    this.settings = {
      totalRounds: 3,
      breathingTime: 30,
      retentionTime: 90
    };

    // Settings elements
    this.settingsBtn = document.getElementById('settingsBtn');
    this.settingsModal = document.getElementById('settingsModal');
    this.cancelSettings = document.getElementById('cancelSettings');
    this.saveSettings = document.getElementById('saveSettings');

    // Bind events
    this.resetBtn.addEventListener('click', () => this.reset());

    // Add circle click handler
    this.breathCircle = document.querySelector('.breath-circle');
    this.breathCircle.addEventListener('click', () => this.toggleTimer());

    // Bind settings events
    this.settingsBtn.addEventListener('click', () => this.openSettings());
    this.cancelSettings.addEventListener('click', () => this.closeSettings());
    this.saveSettings.addEventListener('click', () => this.updateSettings());

    // Initialize inputs and background tap handler
    this.settingsInputs = document.querySelectorAll('.settings-content input');
    this.settingsModal.addEventListener('click', (e) => {
      if (e.target === this.settingsModal) {
        this.closeSettings();
      }
    });

    this.settingsInputs.forEach(input => {
      input.addEventListener('focus', () => {
        // Scroll element into view when focused
        setTimeout(() => {
          input.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 300);
      });
    });

    // Initialize circle
    const circumference = 2 * Math.PI * 156;
    this.progressRing.style.strokeDasharray = `${circumference} ${circumference}`;
    this.progressRing.style.strokeDashoffset = circumference;

    // Load settings
    this.loadSettings();
  }

  loadSettings() {
    const savedSettings = localStorage.getItem('wimHofSettings');
    if (savedSettings) {
      this.settings = JSON.parse(savedSettings);
      this.totalRounds = this.settings.totalRounds;
      this.updateSettingsInputs();
      this.roundDisplay.textContent = `0/${this.settings.totalRounds}`;
    }
  }

  updateSettingsInputs() {
    document.getElementById('roundsInput').value = this.settings.totalRounds;
    document.getElementById('breathingTimeInput').value = this.settings.breathingTime;
    document.getElementById('retentionTimeInput').value = this.settings.retentionTime;
  }

  openSettings() {
    this.updateSettingsInputs();
    this.settingsModal.style.display = 'flex';
    // Reset scroll position when opening
    this.settingsModal.scrollTop = 0;
  }

  closeSettings() {
    this.settingsModal.style.display = 'none';
    this.settingsInputs.forEach(input => input.blur());
  }

  updateSettings() {
    this.settings = {
      totalRounds: parseInt(document.getElementById('roundsInput').value),
      breathingTime: parseInt(document.getElementById('breathingTimeInput').value),
      retentionTime: parseInt(document.getElementById('retentionTimeInput').value)
    };

    localStorage.setItem('wimHofSettings', JSON.stringify(this.settings));
    this.totalRounds = this.settings.totalRounds;

    this.roundDisplay.textContent = `${this.currentRound}/${this.totalRounds}`;

    this.reset();
    this.closeSettings();
  }

  toggleTimer() {
    if (!this.isRunning) {
      if (this.currentPhase === 'ready') {
        this.startSession();
      } else if (this.currentPhase === 'complete') {
        this.reset(); // Reset when clicking circle to start new session
      } else {
        this.isRunning = true;
        this.startTimer();
      }
    } else {
      this.pauseSession();
    }
  }

  startSession() {
    this.isRunning = true;
    this.breathCircle.classList.add('active');
    this.startNextPhase();
  }

  pauseSession() {
    this.isRunning = false;
    this.breathCircle.classList.remove('active');
    clearInterval(this.timerInterval);
  }

  startNextPhase() {
    if (this.currentPhase === 'ready' || this.currentPhase === 'retention') {
      if (this.currentRound >= this.totalRounds) {
        this.completeSession();
        return;
      }
      this.startBreathingPhase();
    } else if (this.currentPhase === 'breathing') {
      this.startRetentionPhase();
    }
  }

  startBreathingPhase() {
    this.currentPhase = 'breathing';
    this.currentRound++;
    this.roundDisplay.textContent = `${this.currentRound}/${this.totalRounds}`;
    this.timeRemaining = this.settings.breathingTime;
    this.phaseDisplay.textContent = 'Deep Breathing';
    this.startTimer();
  }

  startRetentionPhase() {
    this.currentPhase = 'retention';
    this.timeRemaining = this.settings.retentionTime;
    this.phaseDisplay.textContent = 'Breath Retention';
    this.startTimer();
  }

  startTimer() {
    clearInterval(this.timerInterval);
    this.updateDisplay();

    // Add active class if in breathing phase
    if (this.currentPhase === 'breathing') {
      this.breathCircle.classList.add('active');
    }

    this.timerInterval = setInterval(() => {
      this.timeRemaining--;
      this.updateDisplay();

      if (this.timeRemaining <= 0) {
        clearInterval(this.timerInterval);
        if (this.currentPhase === 'breathing' || (this.currentPhase === 'retention' && this.currentRound < this.totalRounds)) {
          this.startNextPhase();
        } else if (this.currentPhase === 'retention' && this.currentRound >= this.totalRounds) {
          this.completeSession();
        }
      }
    }, 1000);
  }

  updateDisplay() {
    const minutes = Math.floor(this.timeRemaining / 60);
    const seconds = this.timeRemaining % 60;
    this.timerDisplay.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;

    // Update progress ring
    const circumference = 2 * Math.PI * 156;
    const totalTime = this.currentPhase === 'breathing' ? this.settings.breathingTime : this.settings.retentionTime;
    const offset = circumference - (this.timeRemaining / totalTime) * circumference;
    this.progressRing.style.strokeDashoffset = offset;
  }

  completeSession() {
    this.isRunning = false;
    this.breathCircle.classList.remove('active');
    this.currentPhase = 'complete';
    this.phaseDisplay.textContent = 'Session Complete!';
    this.timerDisplay.textContent = 'START';
    this.resetBtn.style.display = 'block';
    document.querySelector('.rounds').style.visibility = 'hidden';

    // Add click handler to immediately restart on clicking START
    const restartHandler = () => {
      this.reset();
      this.startSession();
      this.breathCircle.removeEventListener('click', restartHandler);
    };
    this.breathCircle.addEventListener('click', restartHandler);
  }

  reset() {
    clearInterval(this.timerInterval);
    this.breathCircle.classList.remove('active');
    this.currentRound = 0;
    this.isRunning = false;
    this.currentPhase = 'ready';
    this.timeRemaining = 0;
    this.roundDisplay.textContent = `0/${this.totalRounds}`;
    this.phaseDisplay.textContent = 'Ready to begin';
    this.timerDisplay.textContent = 'START';
    this.progressRing.style.strokeDashoffset = 2 * Math.PI * 156;
    document.querySelector('.rounds').style.visibility = 'visible';
  }
}

// Initialize the timer
const wimHofTimer = new WimHofTimer();