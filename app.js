// app.js - PersonaFit Studio

document.addEventListener('DOMContentLoaded', () => {
  // UI Elements - Left Panel
  const uploadZone = document.getElementById('upload-zone');
  const fileInput = document.getElementById('file-input');
  const uploadPlaceholder = document.getElementById('upload-content-placeholder');
  const uploadPreviewContainer = document.getElementById('upload-preview-container');
  const uploadPreviewImg = document.getElementById('upload-preview-img');
  const removeImgBtn = document.getElementById('remove-img-btn');
  
  const presetItems = document.querySelectorAll('.preset-item');
  const customPrompt = document.getElementById('custom-prompt');
  const charCount = document.getElementById('char-count');
  const genderSelect = document.getElementById('gender-select');
  
  const sliderWeight = document.getElementById('slider-weight');
  const sliderWeightVal = document.getElementById('slider-weight-val');
  const sliderCloseness = document.getElementById('slider-closeness');
  const sliderClosenessVal = document.getElementById('slider-closeness-val');
  const sliderDetail = document.getElementById('slider-detail');
  const sliderDetailVal = document.getElementById('slider-detail-val');
  
  const generateBtn = document.getElementById('generate-btn');

  // UI Elements - Right Panel
  const displayFrame = document.getElementById('display-frame');
  const stateUploadRequired = document.getElementById('state-upload-required');
  const stateProcessing = document.getElementById('state-processing');
  const stateReady = document.getElementById('state-ready');
  
  const processingTitle = document.getElementById('processing-title');
  const progressBarFill = document.getElementById('progress-bar-fill');
  const processingStatus = document.getElementById('processing-status');
  
  const comparisonContainer = document.getElementById('comparison-container');
  const beforePanel = document.getElementById('before-panel');
  const afterPanel = document.getElementById('after-panel');
  const imgOriginal = document.getElementById('img-original');
  const imgTransformed = document.getElementById('img-transformed');
  const splitSliderBar = document.getElementById('split-slider-bar');
  
  const canvasControls = document.getElementById('canvas-controls-section');
  const filterContrast = document.getElementById('filter-contrast');
  const filterBrightness = document.getElementById('filter-brightness');
  const filterSaturation = document.getElementById('filter-saturation');

  const snsPresetSelect = document.getElementById('sns-preset-select');
  const snsCropInfo = document.getElementById('sns-crop-info');
  const snsDownloadSection = document.getElementById('sns-download-section');
  
  const actionTools = document.getElementById('action-tools');
  const saveHistoryBtn = document.getElementById('save-history-btn');
  const shareCardBtn = document.getElementById('share-card-btn');
  const downloadLink = document.getElementById('download-link');
  
  const galleryGrid = document.getElementById('gallery-grid');
  const galleryEmpty = document.getElementById('gallery-empty');

  // Header connection components
  const checkConnectionBtn = document.getElementById('check-connection-btn');
  const codexStatusBadge = document.getElementById('codex-status-badge');
  const connectCodexBtn = document.getElementById('connect-codex-btn');
  const loginModal = document.getElementById('login-modal');
  const cancelLoginBtn = document.getElementById('cancel-login-btn');

  // Style Library Elements
  const openLibraryBtn = document.getElementById('open-library-btn');
  const closeLibraryBtn = document.getElementById('close-library-btn');
  const libraryModal = document.getElementById('library-modal');
  const librarySearch = document.getElementById('library-search');
  const libraryGrid = document.getElementById('library-grid');
  const sidebarTabs = document.querySelectorAll('.sidebar-tab');

  // State Variables
  let isImageUploaded = false;
  let userImageSrc = null; // Original source uploaded by user
  let activeStyle = 'professional';
  let isDraggingSlider = false;
  let collection = [];
  let isCodexConnected = false;
  let pollingInterval = null;
  let activeCategory = 'all';
  let detectedImageType = 'person'; // 'person', 'animal', 'object'
  let isAnalyzingImage = false;
  let todayPrompt = '';
  let processingStatusInterval = null;

  // Initialize App
  init();

  function init() {
    loadCollectionFromStorage();
    setupEventListeners();
    checkCodexStatus();
    initLibrary();
    initMinigames();
    fetchTodayStyle();
  }

  // Load collection from localStorage
  function loadCollectionFromStorage() {
    const saved = localStorage.getItem('personafit_collection');
    if (saved) {
      try {
        collection = JSON.parse(saved);
        
        // Sanitize old data: if any item has a massive base64 imgSrc, prune or clean it to free storage!
        let hasLargeItems = false;
        collection = collection.map(item => {
          if (item.imgSrc && item.imgSrc.startsWith('data:') && item.imgSrc.length > 200000) {
            hasLargeItems = true;
            return {
              ...item,
              imgSrc: 'assets/default.png', // fallback placeholder to free up 2-3MB instantly!
              fullImgSrc: null
            };
          }
          return item;
        });

        if (hasLargeItems) {
          localStorage.setItem('personafit_collection', JSON.stringify(collection));
          console.log('Sanitized large items from local storage collection to prevent quota errors.');
        }

        renderGallery();
      } catch (e) {
        console.error('Failed to parse collection', e);
      }
    }
  }

  // Check backend link to Codex CLI doctor status
  function checkCodexStatus() {
    const icon = checkConnectionBtn ? checkConnectionBtn.querySelector('i') : null;
    if (icon) icon.classList.add('spinning');
    if (codexStatusBadge) {
      codexStatusBadge.className = 'status-badge checking';
      codexStatusBadge.textContent = 'Checking Link...';
    }

    fetch('/api/status?_t=' + Date.now())
      .then(res => res.json())
      .then(data => {
        if (icon) icon.classList.remove('spinning');
        if (data.status === 'connected') {
          if (codexStatusBadge) {
            codexStatusBadge.className = 'status-badge connected';
            codexStatusBadge.textContent = 'Codex Connected';
          }
          isCodexConnected = true;
          if (generateBtn) {
            const btnText = generateBtn.querySelector('span');
            if (btnText) btnText.textContent = 'Render Image (이미지 2.0)';
          }
          // 버튼은 항상 표시 - 연결됨 시 Reconnect으로 표시
          if (connectCodexBtn) {
            connectCodexBtn.classList.remove('hidden');
            connectCodexBtn.classList.add('btn-dimmed');
            const lbl = document.getElementById('connect-btn-label');
            if (lbl) lbl.textContent = 'Reconnect';
          }
        } else {
          if (codexStatusBadge) {
            codexStatusBadge.className = 'status-badge disconnected';
            codexStatusBadge.textContent = 'Codex Offline';
          }
          isCodexConnected = false;
          if (generateBtn) {
            const btnText = generateBtn.querySelector('span');
            if (btnText) btnText.textContent = 'Render Style (Mock)';
          }
          if (connectCodexBtn) {
            connectCodexBtn.classList.remove('hidden', 'btn-dimmed');
            const lbl = document.getElementById('connect-btn-label');
            if (lbl) lbl.textContent = 'Login';
          }
        }
      })
      .catch(() => {
        if (icon) icon.classList.remove('spinning');
        if (codexStatusBadge) {
          codexStatusBadge.className = 'status-badge disconnected';
          codexStatusBadge.textContent = 'Connection Error';
        }
        isCodexConnected = false;
        if (generateBtn) {
          const btnText = generateBtn.querySelector('span');
          if (btnText) btnText.textContent = 'Render Style (Mock)';
        }
        if (connectCodexBtn) {
          connectCodexBtn.classList.remove('hidden', 'btn-dimmed');
          const lbl = document.getElementById('connect-btn-label');
          if (lbl) lbl.textContent = 'Login';
        }
      });
  }

  // Start Codex OAuth Login Flow
  function startCodexLogin() {
    if (loginModal) loginModal.classList.remove('hidden');
    
    // Call backend login API to start process and open browser
    fetch('/api/login', { method: 'POST' })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'initiated') {
          startPollingStatus();
        } else {
          alert('로그인 초기화 실패: ' + (data.message || '알 수 없는 오류'));
          closeLoginModal();
        }
      })
      .catch(err => {
        alert('로그인 요청 중 오류 발생: ' + err.message);
        closeLoginModal();
      });
  }

  // Cancel login flow
  function cancelCodexLogin() {
    fetch('/api/login/cancel', { method: 'POST' })
      .then(() => {
        closeLoginModal();
      })
      .catch(() => {
        closeLoginModal();
      });
  }

  function closeLoginModal() {
    if (loginModal) loginModal.classList.add('hidden');
    stopPollingStatus();
    checkCodexStatus();
  }

  function startPollingStatus() {
    if (pollingInterval) clearInterval(pollingInterval);
    
    pollingInterval = setInterval(() => {
      fetch('/api/status?_t=' + Date.now())
        .then(res => res.json())
        .then(data => {
          if (data.status === 'connected') {
            stopPollingStatus();
            if (loginModal) loginModal.classList.add('hidden');
            checkCodexStatus();
            showToast('Codex 연동이 성공적으로 완료되었습니다!', 'success');
          }
        })
        .catch(err => console.error('Polling status failed', err));
    }, 1500);
  }

  function stopPollingStatus() {
    if (pollingInterval) {
      clearInterval(pollingInterval);
      pollingInterval = null;
    }
  }

  // Simple Toast Helper
  function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
      <i data-lucide="check-circle" style="width: 16px; height: 16px; color: #10b981;"></i>
      <span>${message}</span>
    `;
    document.body.appendChild(toast);
    lucide.createIcons();
    
    setTimeout(() => {
      toast.classList.add('show');
    }, 10);

    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }

  // Set up all events
  function setupEventListeners() {
    // Header connection check click
    if (checkConnectionBtn) checkConnectionBtn.addEventListener('click', checkCodexStatus);
    
    // Codex login / connect clicks
    if (connectCodexBtn) connectCodexBtn.addEventListener('click', startCodexLogin);
    if (cancelLoginBtn) cancelLoginBtn.addEventListener('click', cancelCodexLogin);

    // Style Library triggers
    if (openLibraryBtn) openLibraryBtn.addEventListener('click', openLibrary);
    if (closeLibraryBtn) closeLibraryBtn.addEventListener('click', closeLibrary);
    if (librarySearch) librarySearch.addEventListener('input', filterLibrary);

    sidebarTabs.forEach(tab => {
      tab.addEventListener('click', () => {
        sidebarTabs.forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        activeCategory = tab.dataset.category;
        filterLibrary();
      });
    });

    // File Upload Setup
    if (uploadZone) {
      uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('dragover');
      });

      uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('dragover');
      });

      uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length > 0) {
          handleFile(files[0]);
        }
      });
    }

    if (fileInput) {
      fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
          handleFile(e.target.files[0]);
        }
      });
    }

    if (removeImgBtn) {
      removeImgBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        resetUploader();
      });
    }

    presetItems.forEach(item => {
      item.addEventListener('click', () => {
        presetItems.forEach(p => p.classList.remove('active'));
        item.classList.add('active');
        activeStyle = item.dataset.style;
        
        // Populate custom prompt with description if preset selected
        if (customPrompt) {
          if (activeStyle === 'professional') {
            customPrompt.value = 'Professional corporate headshot, dark navy blazer, soft office lighting';
          } else if (activeStyle === 'travel') {
            customPrompt.value = 'Famous global landmark background, beautiful soft lighting, travel photography, highly detailed face, realistic background';
          } else if (activeStyle === 'cinematic') {
            customPrompt.value = 'Dramatic cinematic movie protagonist portrait, moody ambient lighting, highly detailed, film grain, anamorphic lens flare';
          } else if (activeStyle === 'today') {
            customPrompt.value = todayPrompt;
          } else {
            customPrompt.value = '';
          }
          updateCharCount();
        }
      });
    });

    // Prompt Char Counter
    if (customPrompt) {
      customPrompt.addEventListener('input', () => {
        updateCharCount();
      });
    }

    // Slider text bindings
    if (sliderWeight && sliderWeightVal) {
      sliderWeight.addEventListener('input', (e) => {
        sliderWeightVal.textContent = e.target.value;
      });
    }
    if (sliderCloseness && sliderClosenessVal) {
      sliderCloseness.addEventListener('input', (e) => {
        sliderClosenessVal.textContent = `${e.target.value}%`;
      });
    }
    if (sliderDetail && sliderDetailVal) {
      sliderDetail.addEventListener('input', (e) => {
        sliderDetailVal.textContent = `${e.target.value}%`;
      });
    }

    // Generate Button Click
    if (generateBtn) {
      generateBtn.addEventListener('click', () => {
        if (isImageUploaded) {
          runTransformation();
        }
      });
    }

    // Image Split Slider Interactions
    if (splitSliderBar) {
      splitSliderBar.addEventListener('mousedown', (e) => {
        isDraggingSlider = true;
        e.preventDefault();
      });

      splitSliderBar.addEventListener('touchstart', (e) => {
        isDraggingSlider = true;
      });
    }

    window.addEventListener('mouseup', () => {
      isDraggingSlider = false;
    });

    window.addEventListener('mousemove', (e) => {
      if (!isDraggingSlider) return;
      adjustSplitSlider(e.clientX);
    });

    window.addEventListener('touchend', () => {
      isDraggingSlider = false;
    });

    window.addEventListener('touchmove', (e) => {
      if (!isDraggingSlider || e.touches.length === 0) return;
      adjustSplitSlider(e.touches[0].clientX);
    });

    // Filter Controls
    [filterContrast, filterBrightness, filterSaturation].forEach(filter => {
      if (filter) {
        filter.addEventListener('input', applyPostFilters);
      }
    });

    // Save/Collection Actions
    if (saveHistoryBtn) {
      saveHistoryBtn.addEventListener('click', saveToCollection);
    }

    if (shareCardBtn) {
      shareCardBtn.addEventListener('click', generateShareCard);
    }

    if (snsPresetSelect) {
      snsPresetSelect.addEventListener('change', () => {
        const val = snsPresetSelect.value;
        const preset = snsPresets[val];
        if (snsCropInfo && preset) {
          if (val === 'original') {
            snsCropInfo.innerHTML = `Will export as <strong>Original Size</strong>.`;
          } else {
            snsCropInfo.innerHTML = `Will export as <strong>${preset.name}</strong> (${preset.w}x${preset.h}, Aspect ${preset.aspect}) with blurred background padding.`;
          }
        }
        setupDownloadLink();
      });
    }

    if (genderSelect) {
      genderSelect.addEventListener('change', () => {
        const val = genderSelect.value;
        if (val !== 'random' && customPrompt && customPrompt.value.trim() !== '') {
          const adapted = adaptPromptGender(customPrompt.value, val);
          if (adapted !== customPrompt.value) {
            customPrompt.value = adapted;
            updateCharCount();
            showToast(`프롬프트의 성별 표현이 [${val === 'male' ? '남성형' : '여성형'}]으로 자동 조정되었습니다.`, 'success');
          }
        }
      });
    }
  }

  // Handle uploaded file
  function handleFile(file) {
    if (!file.type.startsWith('image/')) {
      alert('이미지 파일만 업로드할 수 있습니다.');
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      userImageSrc = e.target.result;
      uploadPreviewImg.src = userImageSrc;
      
      // Update state
      isImageUploaded = true;
      uploadPlaceholder.classList.add('hidden');
      uploadPreviewContainer.classList.remove('hidden');
      generateBtn.disabled = false;

      // Update right side panel message to prompt instructions
      stateUploadRequired.querySelector('h3').textContent = '셋팅 준비 완료';
      stateUploadRequired.querySelector('p').textContent = '스타일을 선택하거나 프롬프트를 작성하고 아래 생성하기 버튼을 클릭하세요.';

      // Async Image Analysis Trigger
      runImageAnalysis(userImageSrc);
    };
    reader.readAsDataURL(file);
  }

  // Asynchronously query backend to detect gender & image type
  function runImageAnalysis(base64Image) {
    if (!genderSelect) return;
    
    isAnalyzingImage = true;
    detectedImageType = 'person'; // default

    // UI Feedback: disable genderSelect and show indicator
    genderSelect.disabled = true;
    const genderLabel = document.querySelector('.gender-label');
    const originalLabelText = genderLabel ? genderLabel.textContent : 'Gender';
    if (genderLabel) {
      genderLabel.innerHTML = '<span class="status-pulse-dot" style="display:inline-block;width:6px;height:6px;background:#3b82f6;border-radius:50%;margin-right:5px;animation:pulse 1s infinite;"></span>스캔중...';
    }

    fetch('/api/analyze-image', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ image: base64Image })
    })
    .then(res => res.json())
    .then(data => {
      isAnalyzingImage = false;
      genderSelect.disabled = false;
      if (genderLabel) genderLabel.textContent = originalLabelText;

      if (data.type) {
        detectedImageType = data.type;
      }

      // Auto-set gender if the user has not manually changed it yet (currently on 'random')
      if (genderSelect.value === 'random' && data.gender && data.gender !== 'unknown') {
        genderSelect.value = data.gender;
        showToast(`💡 사진 인식 결과: [${data.gender === 'male' ? '남성' : '여성'}] 프로필로 자동 설정되었습니다.`, 'success');
        
        // If there's already a prompt, convert it immediately
        if (customPrompt && customPrompt.value.trim() !== '') {
          const adapted = adaptPromptGender(customPrompt.value, data.gender);
          if (adapted !== customPrompt.value) {
            customPrompt.value = adapted;
            updateCharCount();
          }
        }
      }

      // Face Focus & Auto Crop
      if (data.bbox) {
        cropImageToFace(base64Image, data.bbox, (croppedSrc) => {
          userImageSrc = croppedSrc;
          if (uploadPreviewImg) {
            uploadPreviewImg.src = croppedSrc;
          }
          showToast('📸 최적의 이미지 구도 조정을 위해 얼굴 중심 줌-크롭을 완료했습니다.', 'success');
        });
      }

      if (detectedImageType === 'animal') {
        showToast(`🐾 인식 결과: 반려동물/동물 프로필로 감지되었습니다. 셔플 시 관련 일러스트 스타일이 우선 적용됩니다.`, 'success');
      }
    })
    .catch(err => {
      console.warn('Image analysis failed', err);
      isAnalyzingImage = false;
      genderSelect.disabled = false;
      if (genderLabel) genderLabel.textContent = originalLabelText;
    });
  }

  // Reset Uploader state
  function resetUploader() {
    if (fileInput) fileInput.value = '';
    if (uploadPreviewImg) uploadPreviewImg.src = '';
    userImageSrc = null;
    isImageUploaded = false;
    if (uploadPlaceholder) uploadPlaceholder.classList.remove('hidden');
    if (uploadPreviewContainer) uploadPreviewContainer.classList.add('hidden');
    if (generateBtn) generateBtn.disabled = true;

    // Reset right display states
    if (stateUploadRequired) {
      stateUploadRequired.classList.remove('hidden');
      const h3 = stateUploadRequired.querySelector('h3');
      const p = stateUploadRequired.querySelector('p');
      if (h3) h3.textContent = '업로드된 사진 없음';
      if (p) p.textContent = '왼쪽 패널에서 사진을 먼저 업로드하고 설정을 진행해 주세요.';
    }
    if (stateProcessing) stateProcessing.classList.add('hidden');
    if (stateReady) stateReady.classList.add('hidden');
    
    // Disable controls
    if (canvasControls) canvasControls.classList.add('disabled');
    if (actionTools) actionTools.classList.add('disabled');
    if (snsDownloadSection) snsDownloadSection.classList.add('disabled');
  }

  // Update char counter
  function updateCharCount() {
    if (!customPrompt || !charCount) return;
    const len = customPrompt.value.length;
    if (len > 200) {
      customPrompt.value = customPrompt.value.substring(0, 200);
    }
    charCount.textContent = customPrompt.value.length;
  }

  // Disable / Enable Left Panel Inputs during Rendering
  function setInputState(disabled) {
    if (fileInput) fileInput.disabled = disabled;
    if (customPrompt) customPrompt.disabled = disabled;
    if (genderSelect) genderSelect.disabled = disabled;
    if (sliderWeight) sliderWeight.disabled = disabled;
    if (sliderCloseness) sliderCloseness.disabled = disabled;
    if (sliderDetail) sliderDetail.disabled = disabled;
    if (generateBtn) generateBtn.disabled = disabled || !isImageUploaded;

    const shuffleBtnEl = document.getElementById('shuffle-prompt-btn');
    if (shuffleBtnEl) {
      shuffleBtnEl.disabled = disabled;
      if (disabled) shuffleBtnEl.classList.add('disabled-state');
      else shuffleBtnEl.classList.remove('disabled-state');
    }

    if (removeImgBtn) {
      removeImgBtn.disabled = disabled;
      if (disabled) removeImgBtn.classList.add('disabled-state');
      else removeImgBtn.classList.remove('disabled-state');
    }

    if (openLibraryBtn) {
      openLibraryBtn.disabled = disabled;
      if (disabled) openLibraryBtn.classList.add('disabled-state');
      else openLibraryBtn.classList.remove('disabled-state');
    }

    if (uploadZone) {
      if (disabled) uploadZone.classList.add('disabled-state');
      else uploadZone.classList.remove('disabled-state');
    }

    presetItems.forEach(item => {
      if (disabled) {
        item.classList.add('disabled-state');
      } else {
        item.classList.remove('disabled-state');
      }
    });
  }

  const processingMessages = [
    '얼굴 윤곽 및 이목구비 랜드마크 분석 중...',
    '선택하신 스타일 프리셋 붓터치 맵핑 중...',
    '색조 매트릭스 보정 및 입체적 쉐이딩 적용 중...',
    '얼굴 피부 결 보존 및 미세 텍스처 업스케일링 중...',
    '최종 아티스틱 합성 및 SNS 내보내기 셋팅 준비 중...'
  ];

  function startStatusRolling() {
    if (processingStatusInterval) clearInterval(processingStatusInterval);
    let index = 0;
    processingStatus.textContent = processingMessages[index];
    
    processingStatusInterval = setInterval(() => {
      index = (index + 1) % processingMessages.length;
      processingStatus.textContent = processingMessages[index];
    }, 2000);
  }

  function stopStatusRolling() {
    if (processingStatusInterval) {
      clearInterval(processingStatusInterval);
      processingStatusInterval = null;
    }
  }

  // Simulator Processing Pipeline
  function runTransformation() {
    setInputState(true);
    stateUploadRequired.classList.add('hidden');
    stateReady.classList.add('hidden');
    stateProcessing.classList.remove('hidden');
    
    // Smooth scroll to output canvas to improve mobile usability
    if (displayFrame) {
      displayFrame.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    
    startMinigames();
    startStatusRolling();

    // Reset progress fill
    progressBarFill.style.width = '0%';
    
    if (isCodexConnected) {
      // Real API generation using Codex CLI (async job mode)
      processingTitle.textContent = 'Generating with Image 2.0...';
      processingStatus.textContent = 'Initializing Codex CLI session (Image 2.0)...';
      progressBarFill.style.width = '10%';

      // Slowly increment progress bar while Image 2.0 is generating
      let progress = 10;
      const progressInterval = setInterval(() => {
        if (progress < 90) {
          progress += Math.floor(Math.random() * 4) + 1;
          if (progress > 90) progress = 90;
          progressBarFill.style.width = `${progress}%`;
        }
      }, 700);

      // Step 1: POST to start async job
      fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          image: userImageSrc,
          prompt: customPrompt.value || activeStyle,
          style: activeStyle,
          gender: genderSelect ? genderSelect.value : 'random',
          closeness: sliderCloseness ? parseInt(sliderCloseness.value) : 80,
          weight: sliderWeight ? parseFloat(sliderWeight.value) : 7.5
        })
      })
      .then(res => res.json())
      .then(startData => {
        if (!startData.success || !startData.job_id) {
          throw new Error(startData.error || '작업 시작 실패');
        }

        const jobId = startData.job_id;
        processingStatus.textContent = `Job ${jobId} started — polling for result...`;

        // Step 2: Poll GET /api/generate/{job_id} until done or error
        let attempts = 0;
        const maxAttempts = 100; // 100 × 3s = 5 minutes max

        const pollTimer = setInterval(() => {
          attempts++;
          if (attempts > maxAttempts) {
            clearInterval(pollTimer);
            clearInterval(progressInterval);
            showToast('⚠️ 생성 시간 초과 (5분). 다시 시도해 주세요.', 'error');
            resetProgressState();
            setInputState(false);
            return;
          }

          fetch(`/api/generate/${jobId}?_t=${Date.now()}`)
            .then(r => r.json())
            .then(pollData => {
              if (pollData.status === 'pending') {
                return; // still running — keep polling
              }

              clearInterval(pollTimer);
              clearInterval(progressInterval);

              if (pollData.success && pollData.status === 'done') {
                progressBarFill.style.width = '100%';
                processingStatus.textContent = 'Generation complete!';
                setTimeout(() => {
                  stopMinigames();
                  stateProcessing.classList.add('hidden');
                  stateReady.classList.remove('hidden');
                  imgOriginal.src = userImageSrc;
                  imgTransformed.src = pollData.image;

                  afterPanel.style.width = '50%';
                  splitSliderBar.style.left = '50%';

                  filterContrast.value = 100;
                  filterBrightness.value = 100;
                  filterSaturation.value = 100;
                  imgTransformed.style.filter = 'none';

                  canvasControls.classList.remove('disabled');
                  actionTools.classList.remove('disabled');
                  if (snsDownloadSection) snsDownloadSection.classList.remove('disabled');
                  setupDownloadLink();
                  setInputState(false);
                }, 400);
              } else {
                const errMsg = pollData.error || '알 수 없는 오류';
                stopMinigames();
                resetProgressState();
                setInputState(false);
                showToast('⚠️ 이미지 생성 실패. 다시 시도해 주세요.', 'error');
                console.error('Generation error:', errMsg);
              }
            })
            .catch(err => {
              console.warn('Poll attempt failed, retrying...', err);
              // don't stop — next interval will retry
            });
        }, 3000); // poll every 3 seconds
      })
      .catch(err => {
        clearInterval(progressInterval);
        showToast('⚠️ 네트워크 오류: ' + err.message, 'error');
        resetProgressState();
        setInputState(false);
      });



    } else {
      // Mock / Offline Filter Transformation
      processingTitle.textContent = 'Applying local style filter...';
      const steps = [
        { prg: 25 },
        { prg: 50 },
        { prg: 80 },
        { prg: 100 }
      ];

      let currentStepIdx = 0;
      const interval = setInterval(() => {
        if (currentStepIdx < steps.length) {
          const step = steps[currentStepIdx];
          progressBarFill.style.width = `${step.prg}%`;
          currentStepIdx++;
        } else {
          clearInterval(interval);
          setTimeout(() => {
            finalizeTransformation();
            setInputState(false);
          }, 300);
        }
      }, 1500); // 1.5 seconds per step, 6s total
    }
  }

  function resetProgressState() {
    stopStatusRolling();
    stopMinigames();
    stateProcessing.classList.add('hidden');
    stateUploadRequired.classList.remove('hidden');
    canvasControls.classList.add('disabled');
    actionTools.classList.add('disabled');
    if (snsDownloadSection) snsDownloadSection.classList.add('disabled');
  }

  // Render & setup transformed results for Mock settings
  function finalizeTransformation() {
    stopStatusRolling();
    stopMinigames();
    stateProcessing.classList.add('hidden');
    stateReady.classList.remove('hidden');
    
    // Configure Comparison original image
    imgOriginal.src = userImageSrc;

    // Apply Transformation Logic
    // If user uses default sample avatar face, show pre-generated templates
    const isUsingDefaultMock = userImageSrc.includes('default_avatar') || userImageSrc.startsWith('data:image');
    
    if (isUsingDefaultMock && activeStyle === 'professional') {
      imgTransformed.src = 'assets/professional.png';
    } else {
      applyCanvasStyleTransformation();
    }

    // Reset slider split back to 50%
    afterPanel.style.width = '50%';
    splitSliderBar.style.left = '50%';

    // Reset filters
    filterContrast.value = 100;
    filterBrightness.value = 100;
    filterSaturation.value = 100;
    imgTransformed.style.filter = 'none';

    // Enable panels
    canvasControls.classList.remove('disabled');
    actionTools.classList.remove('disabled');
    if (snsDownloadSection) snsDownloadSection.classList.remove('disabled');

    // Bind Download Trigger
    setupDownloadLink();
  }

  // Core Canvas Engine - transforms custom uploaded photos on client side
  function applyCanvasStyleTransformation() {
    const img = new Image();
    img.src = userImageSrc;
    img.onload = () => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      canvas.width = img.naturalWidth;
      canvas.height = img.naturalHeight;
      
      // Draw base photo
      ctx.drawImage(img, 0, 0);

      // Perform Style Adjustments
      if (activeStyle === 'professional') {
        // Business look: Soft corporate glow and subtle lighting warm gradient
        ctx.globalCompositeOperation = 'source-over';
        ctx.fillStyle = 'rgba(255, 235, 210, 0.08)'; // Warm corporate tint
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Add subtle radial white vignette to center lighting
        const gradient = ctx.createRadialGradient(
          canvas.width / 2, canvas.height / 2, 50,
          canvas.width / 2, canvas.height / 2, canvas.width / 1.2
        );
        gradient.addColorStop(0, 'rgba(255, 255, 255, 0.15)');
        gradient.addColorStop(1, 'rgba(0, 0, 0, 0.15)');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

      } else if (activeStyle === 'travel') {
        // Travel: Sunny warmth and enhanced exposure
        ctx.globalCompositeOperation = 'source-over';
        ctx.fillStyle = 'rgba(255, 220, 160, 0.06)'; // Warm sunlight tint
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Soft gradient overlay to brighten details
        const grad = ctx.createLinearGradient(0, 0, 0, canvas.height);
        grad.addColorStop(0, 'rgba(255, 255, 255, 0.12)'); // Sunny sky glow
        grad.addColorStop(1, 'rgba(0, 0, 0, 0.05)');
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

      } else if (activeStyle === 'cinematic') {
        // Cinematic: Movie moody gradient (teal and orange tones)
        ctx.globalCompositeOperation = 'multiply';
        ctx.fillStyle = 'rgba(25, 45, 55, 0.15)'; // Deep blue-teal shade mapping
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.globalCompositeOperation = 'screen';
        const cinemGrad = ctx.createRadialGradient(
          canvas.width / 2, canvas.height / 2, 20,
          canvas.width / 2, canvas.height / 2, canvas.width / 1.1
        );
        cinemGrad.addColorStop(0, 'rgba(255, 175, 110, 0.28)'); // Warm cinematic spotlight
        cinemGrad.addColorStop(1, 'rgba(10, 30, 45, 0.2)');     // Dark teal vignetting
        ctx.fillStyle = cinemGrad;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
      }

      imgTransformed.src = canvas.toDataURL('image/png');
      setTimeout(setupDownloadLink, 100);
    };
  }

  // Adjust Comparison Split drag position
  function adjustSplitSlider(clientX) {
    const rect = comparisonContainer.getBoundingClientRect();
    let position = clientX - rect.left;
    
    // Clamp values
    if (position < 0) position = 0;
    if (position > rect.width) position = rect.width;

    const percentage = (position / rect.width) * 100;
    afterPanel.style.width = `${percentage}%`;
    splitSliderBar.style.left = `${percentage}%`;
  }

  // Apply Brightness/Contrast/Saturation filter adjustments
  function applyPostFilters() {
    const contrastVal = filterContrast.value;
    const brightnessVal = filterBrightness.value;
    const saturationVal = filterSaturation.value;

    imgTransformed.style.filter = `contrast(${contrastVal}%) brightness(${brightnessVal}%) saturate(${saturationVal}%)`;
    setupDownloadLink();
  }

  const snsPresets = {
    original: { name: 'Original Size (1:1)', w: null, h: null, aspect: '1:1' },
    'x-profile': { name: 'X Profile', w: 400, h: 400, aspect: '1:1' },
    'x-post': { name: 'X Post', w: 1200, h: 675, aspect: '16:9' },
    'linkedin-profile': { name: 'LinkedIn Profile', w: 400, h: 400, aspect: '1:1' },
    'linkedin-post': { name: 'LinkedIn Post', w: 1200, h: 627, aspect: '1.91:1' },
    'threads-profile': { name: 'Threads Profile', w: 320, h: 320, aspect: '1:1' },
    'threads-post': { name: 'Threads Post', w: 1080, h: 1350, aspect: '4:5' },
    'facebook-profile': { name: 'Facebook Profile', w: 170, h: 170, aspect: '1:1' },
    'facebook-post': { name: 'Facebook Post', w: 1200, h: 630, aspect: '1.91:1' },
    'instagram-story': { name: 'Instagram Story', w: 1080, h: 1920, aspect: '9:16' }
  };

  // Render transformed image on high-quality canvas and bind to download tag
  function setupDownloadLink() {
    const presetKey = snsPresetSelect ? snsPresetSelect.value : 'original';
    const preset = snsPresets[presetKey] || snsPresets.original;

    const img = new Image();
    img.src = imgTransformed.src;
    img.onload = () => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      
      const contrastVal = filterContrast.value;
      const brightnessVal = filterBrightness.value;
      const saturationVal = filterSaturation.value;

      // Determine dimensions
      let targetW = preset.w;
      let targetH = preset.h;
      
      if (!targetW || !targetH) {
        targetW = img.naturalWidth || 600;
        targetH = img.naturalHeight || 600;
      }

      canvas.width = targetW;
      canvas.height = targetH;

      const filterStr = `contrast(${contrastVal}%) brightness(${brightnessVal}%) saturate(${saturationVal}%)`;

      if (preset.aspect === '1:1') {
        ctx.filter = filterStr;
        ctx.drawImage(img, 0, 0, targetW, targetH);
      } else {
        // Blurred background cover
        ctx.filter = `${filterStr} blur(30px) brightness(0.35)`;
        
        const imgAspect = img.naturalWidth / img.naturalHeight;
        const targetAspect = targetW / targetH;
        let bgW, bgH, bgX, bgY;
        
        if (imgAspect > targetAspect) {
          bgH = targetH;
          bgW = targetH * imgAspect;
          bgX = (targetW - bgW) / 2;
          bgY = 0;
        } else {
          bgW = targetW;
          bgH = targetW / imgAspect;
          bgX = 0;
          bgY = (targetH - bgH) / 2;
        }
        ctx.drawImage(img, bgX, bgY, bgW, bgH);

        // Center original square avatar
        ctx.filter = filterStr;
        let size = Math.min(targetW, targetH);
        
        if (presetKey === 'instagram-story') {
          size = Math.floor(targetW * 0.65);
        } else {
          size = Math.min(targetW, targetH) - 40;
        }
        
        const cX = (targetW - size) / 2;
        const cY = (targetH - size) / 2;
        
        ctx.drawImage(img, cX, cY, size, size);
      }

      downloadLink.href = canvas.toDataURL('image/png');
      downloadLink.download = `persona-avatar-${presetKey}.png`;
    };
  }

  // Generates a high-quality 1200x600 Before/After share card with vertical split and watermark branding
  function generateShareCard() {
    const imgOrig = new Image();
    imgOrig.crossOrigin = "anonymous";
    imgOrig.src = imgOriginal.src;
    
    const imgTrans = new Image();
    imgTrans.crossOrigin = "anonymous";
    imgTrans.src = imgTransformed.src;

    let loadedCount = 0;
    const onImgLoad = () => {
      loadedCount++;
      if (loadedCount === 2) {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 1200;
        canvas.height = 600;

        // 1. Draw Original (Before) on the Left
        ctx.filter = 'none';
        ctx.drawImage(imgOrig, 0, 0, 600, 600);

        // 2. Draw Transformed (After) on the Right
        const contrastVal = filterContrast.value;
        const brightnessVal = filterBrightness.value;
        const saturationVal = filterSaturation.value;
        ctx.filter = `contrast(${contrastVal}%) brightness(${brightnessVal}%) saturate(${saturationVal}%)`;
        ctx.drawImage(imgTrans, 600, 0, 600, 600);

        // 3. Draw vertical divider down the center
        ctx.filter = 'none';
        ctx.strokeStyle = '#121316';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(600, 0);
        ctx.lineTo(600, 600);
        ctx.stroke();

        // 4. Draw premium branding bar at the bottom
        ctx.fillStyle = 'rgba(12, 13, 15, 0.82)';
        ctx.fillRect(0, 540, 1200, 60);

        // Text - Left side (Branding logo)
        ctx.font = '600 15px Outfit, sans-serif';
        ctx.fillStyle = '#ffffff';
        ctx.textAlign = 'left';
        ctx.textBaseline = 'middle';
        ctx.fillText('PERSONAFIT STUDIO', 40, 570);

        // Text - Right side (URL or tagline)
        ctx.font = '300 13px Inter, sans-serif';
        ctx.fillStyle = '#84868f';
        ctx.textAlign = 'right';
        ctx.fillText('Art-Directed Visual Identity  ·  personafit.ai', 1160, 570);

        // 5. Trigger download
        const link = document.createElement('a');
        link.download = `personafit-share-card-${activeStyle}.png`;
        link.href = canvas.toDataURL('image/png');
        link.click();
      }
    };

    imgOrig.onload = onImgLoad;
    imgTrans.onload = onImgLoad;
    imgOrig.onerror = () => showToast('원본 이미지 로딩 실패', 'error');
    imgTrans.onerror = () => showToast('변환 이미지 로딩 실패', 'error');
  }

  // Helper to compress large base64 images into tiny thumbnails (150x150 JPEG, 60% quality)
  function createThumbnail(src, callback) {
    if (!src || !src.startsWith('data:')) {
      callback(src);
      return;
    }
    const img = new Image();
    img.src = src;
    img.onload = () => {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      canvas.width = 150;
      canvas.height = 150;
      ctx.drawImage(img, 0, 0, 150, 150);
      try {
        const thumb = canvas.toDataURL('image/jpeg', 0.6);
        callback(thumb);
      } catch (err) {
        callback(src);
      }
    };
    img.onerror = () => {
      callback(src);
    };
  }

  // Save Current Styled Avatar to Local Storage Collection
  function saveToCollection() {
    const styleLabelMap = {
      professional: '비즈니스 프로필',
      travel: '여행 테마',
      cinematic: '시네마틱'
    };

    createThumbnail(imgTransformed.src, (thumbSrc) => {
      // Store full image only if it is a URL or a small inline data URL (e.g. < 200KB)
      const isLargeDataUrl = imgTransformed.src.startsWith('data:') && imgTransformed.src.length > 200000;
      const fullImgVal = isLargeDataUrl ? null : imgTransformed.src;

      const newItem = {
        id: 'avatar_' + Date.now(),
        imgSrc: thumbSrc,
        fullImgSrc: fullImgVal,
        style: activeStyle,
        styleLabel: styleLabelMap[activeStyle] || '커스텀 스타일',
        date: new Date().toLocaleDateString('ko-KR', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
        }),
        filters: {
          contrast: filterContrast.value,
          brightness: filterBrightness.value,
          saturation: filterSaturation.value
        }
      };

      collection.unshift(newItem);
      
      try {
        localStorage.setItem('personafit_collection', JSON.stringify(collection));
      } catch (e) {
        console.warn('QuotaExhaustedError: storage full, pruning old items.', e);
        // Prune older collection items to prevent crashing
        if (collection.length > 8) {
          collection = collection.slice(0, 8);
          try {
            localStorage.setItem('personafit_collection', JSON.stringify(collection));
          } catch (e2) {
            console.error('Failed to save collection after pruning:', e2);
          }
        }
      }

      // Add effect & feedback
      saveHistoryBtn.classList.add('disabled-state');
      saveHistoryBtn.innerHTML = '<i data-lucide="check" class="btn-icon-inline"></i><span>저장 완료!</span>';
      lucide.createIcons();

      setTimeout(() => {
        saveHistoryBtn.classList.remove('disabled-state');
        saveHistoryBtn.innerHTML = '<i data-lucide="bookmark" class="btn-icon-inline"></i><span>Add to Collection</span>';
        lucide.createIcons();
      }, 1500);

      renderGallery();
    });
  }

  // Redraw gallery cards
  function renderGallery() {
    if (collection.length === 0) {
      galleryEmpty.classList.remove('hidden');
      return;
    }

    galleryEmpty.classList.add('hidden');
    galleryGrid.querySelectorAll('.gallery-card').forEach(c => c.remove());

    collection.forEach(item => {
      const card = document.createElement('div');
      card.className = 'gallery-card';
      
      const badgeClass = `style-${item.style}`;
      
      card.innerHTML = `
        <div class="gallery-card-img-wrapper">
          <img src="${item.imgSrc}" alt="${item.styleLabel}">
          <span class="gallery-card-badge ${badgeClass}">${item.styleLabel}</span>
          <button class="gallery-card-delete-btn" data-id="${item.id}" title="아바타 삭제">
            <i data-lucide="x" style="width: 14px; height: 14px;"></i>
          </button>
        </div>
        <div class="gallery-card-info">
          <span class="gallery-card-title">${item.styleLabel}</span>
          <span class="gallery-card-date">${item.date}</span>
        </div>
      `;

      // Event listener to delete a single item
      card.querySelector('.gallery-card-delete-btn').addEventListener('click', (e) => {
        e.stopPropagation();
        deleteCollectionItem(item.id);
      });

      // Event listener to reload history item back to canvas for review
      card.addEventListener('click', () => {
        imgOriginal.src = userImageSrc || item.fullImgSrc || item.imgSrc;
        imgTransformed.src = item.fullImgSrc || item.imgSrc;
        
        filterContrast.value = item.filters.contrast || 100;
        filterBrightness.value = item.filters.brightness || 100;
        filterSaturation.value = item.filters.saturation || 100;
        imgTransformed.style.filter = `contrast(${filterContrast.value}%) brightness(${filterBrightness.value}%) saturate(${filterSaturation.value}%)`;

        stateUploadRequired.classList.add('hidden');
        stateProcessing.classList.add('hidden');
        stateReady.classList.remove('hidden');

        canvasControls.classList.remove('disabled');
        actionTools.classList.remove('disabled');
        if (snsDownloadSection) snsDownloadSection.classList.remove('disabled');
        setupDownloadLink();
      });

      galleryGrid.appendChild(card);
    });

    lucide.createIcons();
  }

  // Delete a saved avatar
  function deleteCollectionItem(id) {
    collection = collection.filter(item => item.id !== id);
    try {
      localStorage.setItem('personafit_collection', JSON.stringify(collection));
    } catch (e) {
      console.error('Failed to update storage after deletion:', e);
    }
    renderGallery();
  }



  // ========================
  // REACTOR PROMPT LIBRARY (1800개 라이브 연동)
  // ========================

  let allPrompts = [];       // 전체 1800개 캐시
  let filteredPrompts = [];  // 필터된 결과
  let currentPage = 0;
  const PAGE_SIZE = 24;
  let isLoadingMore = false;
  let activeLibCategory = 'all';

  // 카테고리 → 자동 슬라이더 튜닝 테이블
  const categoryTuning = {
    portrait: { weight: 6.5, closeness: 85, detail: 45 },
    photo:    { weight: 6.5, closeness: 85, detail: 45 },
    cosplay:  { weight: 9.5, closeness: 55, detail: 65 },
    character:{ weight: 9.5, closeness: 55, detail: 65 },
    illustration:{ weight: 9.0, closeness: 60, detail: 60 },
    plush:    { weight: 8.5, closeness: 65, detail: 50 },
    sticker:  { weight: 8.0, closeness: 65, detail: 55 },
    food:     { weight: 7.0, closeness: 75, detail: 55 },
    product:  { weight: 7.0, closeness: 75, detail: 55 },
    poster:   { weight: 8.5, closeness: 60, detail: 60 },
    infographic:{ weight: 7.5, closeness: 70, detail: 50 },
    design:   { weight: 7.5, closeness: 70, detail: 50 },
    other:    { weight: 7.5, closeness: 70, detail: 50 }
  };

  function fetchTodayStyle() {
    fetch('/api/today-style')
      .then(r => r.json())
      .then(data => {
        const descEl = document.getElementById('today-preset-desc');
        const nameEl = document.getElementById('today-preset-name');
        if (descEl) {
          descEl.textContent = data.description || '';
          descEl.title = data.theme || '';
        }
        if (nameEl && data.theme) {
          nameEl.textContent = data.theme;
        }
        todayPrompt = data.prompt || '';
      })
      .catch(err => {
        console.error('Failed to fetch today style:', err);
        const descEl = document.getElementById('today-preset-desc');
        if (descEl) descEl.textContent = '불러오기 실패';
      });
  }

  function initLibrary() {
    // gallery-data.json 비동기 로드
    fetch('/gallery-data.json?_t=' + Date.now())
      .then(r => r.json())
      .then(data => {
        allPrompts = (data.posts || []).filter(p => p.prompt && p.prompt.trim());
        updateLibraryCount();
        // 내장 DB는 fallback용으로 유지 (필요 시 아래 stylePresetsDatabase 사용)
      })
      .catch(err => {
        console.warn('gallery-data.json 로드 실패, 내장 DB 사용:', err);
        allPrompts = stylePresetsDatabase.map(s => ({
          id: s.id,
          caption: s.title,
          prompt: s.prompt,
          thumbnail: null,
          tags: [s.category]
        }));
        updateLibraryCount();
      });
  }

  function updateLibraryCount() {
    const badge = document.getElementById('library-count-badge');
    if (badge) badge.textContent = `${allPrompts.length.toLocaleString()}개 프롬프트`;
  }

  function openLibrary() {
    if (libraryModal) {
      libraryModal.classList.remove('hidden');
      if (librarySearch) {
        librarySearch.value = '';
        librarySearch.focus();
      }
      activeLibCategory = 'all';
      document.querySelectorAll('.sidebar-tab').forEach(t => t.classList.remove('active'));
      const allTab = document.querySelector('.sidebar-tab[data-category="all"]');
      if (allTab) allTab.classList.add('active');
      resetAndRender();
    }
  }

  function closeLibrary() {
    if (libraryModal) libraryModal.classList.add('hidden');
  }

  function resetAndRender() {
    currentPage = 0;
    filteredPrompts = getFiltered();
    libraryGrid.innerHTML = '';
    renderPage();
    // 무한 스크롤 바인딩
    const gridContainer = document.querySelector('.library-grid-container');
    if (gridContainer) {
      gridContainer.onscroll = () => {
        if (gridContainer.scrollTop + gridContainer.clientHeight >= gridContainer.scrollHeight - 200) {
          if (!isLoadingMore && currentPage * PAGE_SIZE < filteredPrompts.length) {
            renderPage();
          }
        }
      };
    }
  }

  function getFiltered() {
    const query = librarySearch ? librarySearch.value.toLowerCase().trim() : '';
    return allPrompts.filter(p => {
      const catMatch = (activeLibCategory === 'all') ||
        (p.tags && p.tags.some(t => t.toLowerCase() === activeLibCategory));
      const qMatch = !query ||
        (p.caption && p.caption.toLowerCase().includes(query)) ||
        (p.prompt && p.prompt.toLowerCase().includes(query));
      return catMatch && qMatch;
    });
  }

  function renderPage() {
    isLoadingMore = true;
    const start = currentPage * PAGE_SIZE;
    const end = Math.min(start + PAGE_SIZE, filteredPrompts.length);
    const slice = filteredPrompts.slice(start, end);

    if (start === 0 && slice.length === 0) {
      libraryGrid.innerHTML = '<p style="grid-column:1/-1;text-align:center;color:var(--text-muted);padding:40px 0;">검색 결과가 없습니다.</p>';
      isLoadingMore = false;
      return;
    }

    slice.forEach(post => {
      const card = document.createElement('div');
      card.className = 'style-card reactor-card';
      card.addEventListener('click', () => applyReactorStyle(post));

      const imgSrc = post.thumbnail;

      const tags = (post.tags || ['other']);
      const tagHTML = tags.map(t => `<span class="reactor-tag">${t}</span>`).join('');

      const captionShort = (post.caption || '').replace(/\n/g, ' ').substring(0, 60);
      const promptShort = (post.prompt || '').substring(0, 80);

      card.innerHTML = `
        <div class="style-card-preview reactor-preview">
          ${imgSrc
            ? `<img src="${imgSrc}" loading="lazy" alt="preview" onerror="if(!this.dataset.fallback){this.dataset.fallback='true';this.src='https://reactorprompt.vercel.app'+this.getAttribute('src');}else{this.parentNode.style.background='linear-gradient(135deg,#1f2937,#111827)';this.remove();}">`
            : `<div class="no-thumb-placeholder"><i data-lucide="image" style="width:32px;height:32px;opacity:0.3;"></i></div>`
          }
          <div class="reactor-tag-row">${tagHTML}</div>
        </div>
        <div class="style-card-info">
          <h4 class="style-card-title">${captionShort || '(제목 없음)'}</h4>
          <p class="style-card-desc">${promptShort}...</p>
        </div>
      `;
      libraryGrid.appendChild(card);
    });

    lucide.createIcons();
    currentPage++;
    isLoadingMore = false;
  }

  function filterLibrary() {
    resetAndRender();
  }

  function applyReactorStyle(post) {
    // 프롬프트 주입
    if (customPrompt) {
      let promptText = (post.prompt || '').substring(0, 200);
      const currentGender = genderSelect ? genderSelect.value : 'random';
      if (currentGender !== 'random') {
        promptText = adaptPromptGender(promptText, currentGender);
      }
      customPrompt.value = promptText;
      updateCharCount();
    }

    // 카테고리 기반 자동 슬라이더 튜닝
    const primaryTag = (post.tags && post.tags[0]) || 'other';
    const tuning = categoryTuning[primaryTag] || categoryTuning.other;

    if (sliderWeight) {
      sliderWeight.value = tuning.weight;
      sliderWeightVal.textContent = tuning.weight;
    }
    if (sliderCloseness) {
      sliderCloseness.value = tuning.closeness;
      sliderClosenessVal.textContent = `${tuning.closeness}%`;
    }
    if (sliderDetail) {
      sliderDetail.value = tuning.detail;
      sliderDetailVal.textContent = `${tuning.detail}%`;
    }

    presetItems.forEach(p => p.classList.remove('active'));
    activeStyle = 'custom';

    closeLibrary();
    showToast(`스타일 프롬프트가 적용되었습니다. 매개변수도 자동 튜닝 완료!`, 'success');
  }

  // 랜덤 셔플 - 1800개 중 무작위 1개 즉시 적용
  function shuffleRandomStyle() {
    if (allPrompts.length === 0) {
      showToast('프롬프트 DB 로딩 중입니다. 잠시 후 다시 시도해 주세요.', 'error');
      return;
    }

    let targetPrompts = allPrompts;

    if (detectedImageType === 'animal' || detectedImageType === 'object') {
      const filtered = allPrompts.filter(p => {
        const tags = p.tags || [];
        return tags.some(t => ['illustration', 'sticker', 'character', 'other', 'poster'].includes(t.toLowerCase()));
      });
      if (filtered.length > 0) {
        targetPrompts = filtered;
      }
    } else {
      const filtered = allPrompts.filter(p => {
        const tags = p.tags || [];
        return tags.some(t => ['portrait', 'photo', 'cosplay', 'character'].includes(t.toLowerCase()));
      });
      if (filtered.length > 0) {
        targetPrompts = filtered;
      }
    }

    const rnd = targetPrompts[Math.floor(Math.random() * targetPrompts.length)];
    applyReactorStyleDirect(rnd);
  }

  function applyReactorStyleDirect(post) {
    if (customPrompt) {
      let promptText = (post.prompt || '').substring(0, 200);
      let currentGender = genderSelect ? genderSelect.value : 'random';
      if (currentGender === 'random') {
        currentGender = Math.random() < 0.5 ? 'male' : 'female';
        if (genderSelect) {
          genderSelect.value = currentGender;
        }
      }
      promptText = adaptPromptGender(promptText, currentGender);
      customPrompt.value = promptText;
      updateCharCount();
    }
    const primaryTag = (post.tags && post.tags[0]) || 'other';
    const tuning = categoryTuning[primaryTag] || categoryTuning.other;
    if (sliderWeight) { sliderWeight.value = tuning.weight; sliderWeightVal.textContent = tuning.weight; }
    if (sliderCloseness) { sliderCloseness.value = tuning.closeness; sliderClosenessVal.textContent = `${tuning.closeness}%`; }
    if (sliderDetail) { sliderDetail.value = tuning.detail; sliderDetailVal.textContent = `${tuning.detail}%`; }
    presetItems.forEach(p => p.classList.remove('active'));
    activeStyle = 'custom';
    showToast(`🎲 랜덤 스타일 적용: 태그 [${(post.tags||['other']).join(', ')}]`, 'success');
  }

  // ========================
  // 기존 내장 DB (Fallback)
  // ========================
  const stylePresetsDatabase = [
    { id: 'studio_classic', title: '시네마틱 스튜디오', category: 'portrait',
      prompt: 'Professional corporate headshot, 8k resolution, photorealistic, cinematic lighting, portrait photography, detailed skin texture, crisp focus, neutral studio background',
      bg: 'linear-gradient(135deg, #1f2937, #111827)' },
    { id: 'neon_noir', title: '네온 느와르', category: 'portrait',
      prompt: 'Moody cinematic portrait, high contrast dark atmosphere, subtle neon red ambient lighting, realistic, detailed reflections',
      bg: 'linear-gradient(135deg, #4c1d95, #111827)' },
    { id: 'anime_ghibli', title: '지브리 감성', category: 'illustration',
      prompt: 'Anime character portrait, Studio Ghibli aesthetic, hand-drawn digital illustration, soft pastel colors, whimsical mood',
      bg: 'linear-gradient(135deg, #10b981, #065f46)' },
    { id: 'cyberpunk_classic', title: '네온 디스토피아', category: 'cosplay',
      prompt: 'Futuristic cyberpunk portrait, neon magenta and cyan highlights, glowing cybernetic visor, highly detailed, octane render, techwear aesthetic',
      bg: 'linear-gradient(135deg, #ec4899, #06b6d4)' },
    { id: 'oil_painting', title: '고전 유화', category: 'illustration',
      prompt: 'Classical oil painting portrait, Rembrandt lighting style, textured thick brush strokes, fine art museum aesthetic, dramatic shadows',
      bg: 'linear-gradient(135deg, #78350f, #1e1b4b)' },
  ];

  // 사이드바 탭 이벤트 재바인딩 (카테고리 변수 activeLibCategory 사용)
  sidebarTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      sidebarTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      activeLibCategory = tab.dataset.category;
      filterLibrary();
    });
  });

  // 랜덤 셔플 버튼 바인딩
  const shuffleBtn = document.getElementById('shuffle-prompt-btn');
  if (shuffleBtn) shuffleBtn.addEventListener('click', shuffleRandomStyle);

  // ========================
  // MINI-GAME ENGINE SET
  // ========================
  let memoryTimerInterval = null;
  let memoryTime = 0;
  let memoryMoves = 0;
  let firstFlippedCard = null;
  let secondFlippedCard = null;
  let memoryMatchedCount = 0;
  let isCheckingMatch = false;

  let tttBoard = Array(9).fill('');
  let tttActive = true;
  let isAiThinking = false;

  function initMinigames() {
    const tabMemory = document.getElementById('tab-memory');
    const tabTictactoe = document.getElementById('tab-tictactoe');
    const gameMemoryContainer = document.getElementById('game-memory-container');
    const gameTictactoeContainer = document.getElementById('game-tictactoe-container');
    const minigameRestart = document.getElementById('minigame-restart');
    const tttRestart = document.getElementById('ttt-restart');

    if (tabMemory && tabTictactoe && gameMemoryContainer && gameTictactoeContainer) {
      tabMemory.addEventListener('click', () => {
        tabMemory.classList.add('active');
        tabTictactoe.classList.remove('active');
        gameMemoryContainer.classList.remove('hidden');
        gameTictactoeContainer.classList.add('hidden');
      });

      tabTictactoe.addEventListener('click', () => {
        tabMemory.classList.remove('active');
        tabTictactoe.classList.add('active');
        gameMemoryContainer.classList.add('hidden');
        gameTictactoeContainer.classList.remove('hidden');
      });
    }

    if (minigameRestart) {
      minigameRestart.addEventListener('click', () => resetMemoryGame());
    }
    if (tttRestart) {
      tttRestart.addEventListener('click', () => resetTttGame());
    }
  }

  function startMinigames() {
    const minigameWrapper = document.getElementById('minigame-wrapper');
    if (minigameWrapper) {
      minigameWrapper.classList.remove('hidden');
    }
    resetMemoryGame();
    resetTttGame();
  }

  function stopMinigames() {
    const minigameWrapper = document.getElementById('minigame-wrapper');
    if (minigameWrapper) {
      minigameWrapper.classList.add('hidden');
    }
    if (memoryTimerInterval) {
      clearInterval(memoryTimerInterval);
      memoryTimerInterval = null;
    }
  }

  // --- Game 1: Memory Match ---
  function resetMemoryGame() {
    const grid = document.getElementById('minigame-grid');
    const movesText = document.getElementById('minigame-moves');
    const timerText = document.getElementById('minigame-timer');

    if (!grid) return;

    if (memoryTimerInterval) clearInterval(memoryTimerInterval);
    memoryTimerInterval = null;
    memoryTime = 0;
    memoryMoves = 0;
    firstFlippedCard = null;
    secondFlippedCard = null;
    memoryMatchedCount = 0;
    isCheckingMatch = false;

    if (movesText) movesText.textContent = '0 moves';
    if (timerText) timerText.textContent = '0:00';

    const emojis = ['🎨', '📷', '💻', '🧠', '🎮', '🚀', '⚡', '🔮'];
    const cards = [...emojis, ...emojis];
    
    for (let i = cards.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [cards[i], cards[j]] = [cards[j], cards[i]];
    }

    grid.innerHTML = '';
    cards.forEach((emoji, index) => {
      const cardEl = document.createElement('div');
      cardEl.className = 'card';
      cardEl.dataset.index = index;
      cardEl.dataset.value = emoji;
      cardEl.addEventListener('click', () => handleCardClick(cardEl));
      grid.appendChild(cardEl);
    });

    memoryTimerInterval = setInterval(() => {
      memoryTime++;
      const mins = Math.floor(memoryTime / 60);
      const secs = String(memoryTime % 60).padStart(2, '0');
      if (timerText) timerText.textContent = `${mins}:${secs}`;
    }, 1000);
  }

  function handleCardClick(cardEl) {
    if (isCheckingMatch) return;
    if (cardEl.classList.contains('revealed') || cardEl.classList.contains('matched')) return;

    cardEl.classList.add('revealed');
    cardEl.textContent = cardEl.dataset.value;

    if (!firstFlippedCard) {
      firstFlippedCard = cardEl;
    } else {
      secondFlippedCard = cardEl;
      checkMemoryMatch();
    }
  }

  function checkMemoryMatch() {
    isCheckingMatch = true;
    memoryMoves++;
    
    const movesText = document.getElementById('minigame-moves');
    if (movesText) {
      movesText.textContent = `${memoryMoves} move${memoryMoves > 1 ? 's' : ''}`;
    }

    const val1 = firstFlippedCard.dataset.value;
    const val2 = secondFlippedCard.dataset.value;

    if (val1 === val2) {
      setTimeout(() => {
        firstFlippedCard.classList.remove('revealed');
        firstFlippedCard.classList.add('matched');
        secondFlippedCard.classList.remove('revealed');
        secondFlippedCard.classList.add('matched');

        firstFlippedCard = null;
        secondFlippedCard = null;
        isCheckingMatch = false;

        memoryMatchedCount += 2;
        if (memoryMatchedCount === 16) {
          clearInterval(memoryTimerInterval);
          showToast(`🎉 축하합니다! Memory Match 성공! (Moves: ${memoryMoves})`, 'success');
        }
      }, 300);
    } else {
      setTimeout(() => {
        firstFlippedCard.classList.remove('revealed');
        firstFlippedCard.textContent = '';
        secondFlippedCard.classList.remove('revealed');
        secondFlippedCard.textContent = '';

        firstFlippedCard = null;
        secondFlippedCard = null;
        isCheckingMatch = false;
      }, 800);
    }
  }

  // --- Game 2: Tic-Tac-Toe ---
  function resetTttGame() {
    const grid = document.getElementById('ttt-grid');
    const statusText = document.getElementById('ttt-status');

    if (!grid) return;

    tttBoard = Array(9).fill('');
    tttActive = true;
    isAiThinking = false;

    if (statusText) statusText.textContent = 'Your turn (X)';

    grid.innerHTML = '';
    for (let i = 0; i < 9; i++) {
      const cellEl = document.createElement('div');
      cellEl.className = 'ttt-cell';
      cellEl.dataset.index = i;
      cellEl.addEventListener('click', () => handleTttClick(cellEl, i));
      grid.appendChild(cellEl);
    }
  }

  function handleTttClick(cellEl, index) {
    if (!tttActive || isAiThinking || tttBoard[index] !== '') return;

    tttBoard[index] = 'X';
    cellEl.textContent = 'X';
    cellEl.classList.add('taken', 'x-player');

    if (checkTttWinner('X')) {
      tttActive = false;
      const statusText = document.getElementById('ttt-status');
      if (statusText) statusText.textContent = 'You won! 🎉';
      showToast('❌ 당신이 이겼습니다! ⭕', 'success');
      return;
    }

    if (tttBoard.every(cell => cell !== '')) {
      tttActive = false;
      const statusText = document.getElementById('ttt-status');
      if (statusText) statusText.textContent = "It's a draw!";
      return;
    }

    isAiThinking = true;
    const statusText = document.getElementById('ttt-status');
    if (statusText) statusText.textContent = 'AI is thinking...';

    setTimeout(() => {
      if (!tttActive) return;
      makeAiMove();
      isAiThinking = false;
    }, 450);
  }

  function makeAiMove() {
    let aiIndex = findWinningMove('O');
    if (aiIndex === -1) {
      aiIndex = findWinningMove('X');
    }
    if (aiIndex === -1 && tttBoard[4] === '') {
      aiIndex = 4;
    }
    if (aiIndex === -1) {
      const emptyIndices = tttBoard.map((val, idx) => val === '' ? idx : null).filter(val => val !== null);
      if (emptyIndices.length > 0) {
        aiIndex = emptyIndices[Math.floor(Math.random() * emptyIndices.length)];
      }
    }

    if (aiIndex !== -1) {
      tttBoard[aiIndex] = 'O';
      const grid = document.getElementById('ttt-grid');
      if (grid) {
        const cellEl = grid.children[aiIndex];
        if (cellEl) {
          cellEl.textContent = 'O';
          cellEl.classList.add('taken', 'o-ai');
        }
      }

      if (checkTttWinner('O')) {
        tttActive = false;
        const statusText = document.getElementById('ttt-status');
        if (statusText) statusText.textContent = 'AI won! 🤖';
        return;
      }

      if (tttBoard.every(cell => cell !== '')) {
        tttActive = false;
        const statusText = document.getElementById('ttt-status');
        if (statusText) statusText.textContent = "It's a draw!";
        return;
      }
    }

    const statusText = document.getElementById('ttt-status');
    if (statusText) statusText.textContent = 'Your turn (X)';
  }

  function findWinningMove(player) {
    const winningCombos = [
      [0, 1, 2], [3, 4, 5], [6, 7, 8],
      [0, 3, 6], [1, 4, 7], [2, 5, 8],
      [0, 4, 8], [2, 4, 6]
    ];

    for (let combo of winningCombos) {
      const count = combo.filter(idx => tttBoard[idx] === player).length;
      const empty = combo.filter(idx => tttBoard[idx] === '').length;
      if (count === 2 && empty === 1) {
        return combo.find(idx => tttBoard[idx] === '');
      }
    }
    return -1;
  }

  function checkTttWinner(player) {
    const winningCombos = [
      [0, 1, 2], [3, 4, 5], [6, 7, 8],
      [0, 3, 6], [1, 4, 7], [2, 5, 8],
      [0, 4, 8], [2, 4, 6]
    ];

    return winningCombos.some(combo => {
      return combo.every(idx => tttBoard[idx] === player);
    });
  }

  function adaptPromptGender(prompt, targetGender) {
    if (!prompt || (targetGender !== 'male' && targetGender !== 'female')) return prompt;

    const femaleToMale = [
      { f: 'woman', m: 'man' },
      { f: 'women', m: 'men' },
      { f: 'girl', m: 'boy' },
      { f: 'girls', m: 'boys' },
      { f: 'female', m: 'male' },
      { f: 'lady', m: 'gentleman' },
      { f: 'ladies', m: 'gentlemen' },
      { f: 'goddess', m: 'god' },
      { f: 'herself', m: 'himself' },
      { f: 'she', m: 'he' },
      { f: 'her', m: 'his' },
      { f: 'dress', m: 'suit' },
      { f: 'skirt', m: 'pants' },
      { f: 'makeup', m: 'grooming' },
      { f: 'blouse', m: 'shirt' }
    ];

    const maleToFemale = [
      { m: 'man', f: 'woman' },
      { m: 'men', f: 'women' },
      { m: 'boy', f: 'girl' },
      { m: 'boys', f: 'girls' },
      { m: 'male', f: 'female' },
      { m: 'gentleman', f: 'lady' },
      { m: 'gentlemen', f: 'ladies' },
      { m: 'guy', f: 'girl' },
      { m: 'guys', f: 'girls' },
      { m: 'god', f: 'goddess' },
      { m: 'himself', f: 'herself' },
      { m: 'he', f: 'she' },
      { m: 'his', f: 'her' },
      { m: 'suit', f: 'dress' },
      { m: 'pants', f: 'skirt' },
      { m: 'grooming', f: 'makeup' },
      { m: 'shirt', f: 'blouse' }
    ];

    let result = prompt;

    function replaceWord(text, fromWord, toWord) {
      const patterns = [
        { regex: new RegExp('\\b' + fromWord + '\\b', 'g'), replacement: toWord },
        { regex: new RegExp('\\b' + fromWord.charAt(0).toUpperCase() + fromWord.slice(1) + '\\b', 'g'), 
          replacement: toWord.charAt(0).toUpperCase() + toWord.slice(1) },
        { regex: new RegExp('\\b' + fromWord.toUpperCase() + '\\b', 'g'), replacement: toWord.toUpperCase() }
      ];
      
      let temp = text;
      patterns.forEach(p => {
        temp = temp.replace(p.regex, p.replacement);
      });
      return temp;
    }

    if (targetGender === 'male') {
      femaleToMale.forEach(pair => {
        result = replaceWord(result, pair.f, pair.m);
      });
    } else if (targetGender === 'female') {
      maleToFemale.forEach(pair => {
        result = replaceWord(result, pair.m, pair.f);
      });
    }

    return result;
  }

  function cropImageToFace(base64Src, bbox, callback) {
    if (!bbox || bbox.length !== 4) {
      callback(base64Src);
      return;
    }

    const img = new Image();
    img.src = base64Src;
    img.onload = () => {
      const width = img.naturalWidth;
      const height = img.naturalHeight;

      const ymin = (bbox[0] / 100) * height;
      const xmin = (bbox[1] / 100) * width;
      const ymax = (bbox[2] / 100) * height;
      const xmax = (bbox[3] / 100) * width;

      const fW = xmax - xmin;
      const fH = ymax - ymin;
      const fSize = Math.max(fW, fH);
      const centerX = xmin + fW / 2;
      const centerY = ymin + fH / 2;

      // Zoom focus box (1.7x face size)
      let cropSize = fSize * 1.7;
      const maxPossibleSize = Math.min(width, height);
      if (cropSize > maxPossibleSize) {
        cropSize = maxPossibleSize;
      }

      let cropX = centerX - cropSize / 2;
      let cropY = centerY - cropSize / 2;

      if (cropX < 0) {
        cropX = 0;
      } else if (cropX + cropSize > width) {
        cropX = width - cropSize;
      }

      if (cropY < 0) {
        cropY = 0;
      } else if (cropY + cropSize > height) {
        cropY = height - cropSize;
      }

      const canvas = document.createElement('canvas');
      canvas.width = 600;
      canvas.height = 600;
      const ctx = canvas.getContext('2d');

      ctx.drawImage(
        img,
        Math.floor(cropX), Math.floor(cropY), Math.floor(cropSize), Math.floor(cropSize),
        0, 0, 600, 600
      );

      try {
        const croppedSrc = canvas.toDataURL('image/png');
        callback(croppedSrc);
      } catch (err) {
        console.warn('Canvas crop failed, fallback to original', err);
        callback(base64Src);
      }
    };

    img.onerror = () => {
      callback(base64Src);
    };
  }

});
