/**
 * PromptCraft AI — Frontend JavaScript
 * Universal Prompt Generator & Quality Evaluator
 * College Subject: Introduction to Prompt Engineering (IPE)
 */

document.addEventListener('DOMContentLoaded', () => {
  // -------------------------------------------------------------------------
  // DOM ELEMENTS
  // -------------------------------------------------------------------------
  const generatorForm = document.getElementById('generator-form');
  const generateBtn = document.getElementById('generate-btn');
  const btnSpinner = document.getElementById('btn-spinner');
  const btnTextContent = document.getElementById('btn-text-content');
  
  const categoryCards = document.querySelectorAll('.category-card');
  const selectedCategoryInput = document.getElementById('selected-category');
  const activeCategoryDisplay = document.getElementById('active-category-display');
  const categoryHintBox = document.getElementById('category-hint');
  const categoryHintText = document.getElementById('category-hint-text');
  
  const ideaInput = document.getElementById('idea-input');
  const ideaCharCount = document.getElementById('idea-char-count');
  const ideaErrorMsg = document.getElementById('idea-error-msg');
  const clearIdeaBtn = document.getElementById('clear-idea-btn');
  
  const styleRadios = document.querySelectorAll('input[name="style"]');
  const activeStyleDisplay = document.getElementById('active-style-display');
  
  const instructionsInput = document.getElementById('instructions-input');
  const instructionsCharCount = document.getElementById('instructions-char-count');
  const instructionsAccordion = document.querySelector('.instructions-accordion');
  
  // Output elements
  const outputPanel = document.getElementById('output-panel');
  const outputCategoryBadge = document.getElementById('output-category-badge');
  const outputStyleBadge = document.getElementById('output-style-badge');
  const outputWordCount = document.getElementById('output-word-count');
  const outputOriginalIdea = document.getElementById('output-original-idea');
  const promptOutputText = document.getElementById('prompt-output-text');
  
  const copyBtn = document.getElementById('copy-btn');
  const copyText = document.getElementById('copy-text');
  const regenerateBtn = document.getElementById('regenerate-btn');
  const clearOutputBtn = document.getElementById('clear-output-btn');
  
  // Quality check elements
  const qualityScoreValue = document.getElementById('quality-score-value');
  const qualityRatingLabel = document.getElementById('quality-rating-label');
  const qualityProgressFill = document.getElementById('quality-progress-fill');
  const rubricClarity = document.getElementById('rubric-clarity');
  const barClarity = document.getElementById('bar-clarity');
  const rubricContext = document.getElementById('rubric-context');
  const barContext = document.getElementById('bar-context');
  const rubricSpecificity = document.getElementById('rubric-specificity');
  const barSpecificity = document.getElementById('bar-specificity');
  const rubricFormat = document.getElementById('rubric-format');
  const barFormat = document.getElementById('bar-format');
  const qualitySuggestionsList = document.getElementById('quality-suggestions-list');
  const qualityDisclaimer = document.getElementById('quality-disclaimer');
  
  // Toast & Mobile Nav
  const toast = document.getElementById('toast');
  const toastMessage = document.getElementById('toast-message');
  const mobileToggle = document.getElementById('mobile-toggle');
  const navLinks = document.getElementById('nav-links');
  
  // Quick Examples Buttons
  const exampleLoadButtons = document.querySelectorAll('.btn-example-load');

  // State
  let currentVariation = 0;
  let isSubmitting = false;

  // Category Configuration (Hints & Placeholders)
  const CATEGORY_META = {
    image: {
      label: "Image Generation",
      icon: "🖼️",
      placeholder: "e.g. A sprawling cyberpunk city at midnight with neon violet skyscrapers and flying vehicles in heavy rain...",
      hint: "<strong>Image Tip:</strong> Mention subject, camera angle (wide, macro), lighting (neon rim, volumetric), and rendering style (octane, 8K, photorealistic)."
    },
    video: {
      label: "Video Generation",
      icon: "🎬",
      placeholder: "e.g. A barista pouring intricate latte art in slow motion inside a cozy coffee shop on a rainy morning...",
      hint: "<strong>Video Tip:</strong> Specify camera movement (drone push, orbiting, tracking), pacing/fps, lighting changes, and environmental Foley sounds."
    },
    website: {
      label: "Website Creation",
      icon: "🌐",
      placeholder: "e.g. A futuristic portfolio website for an AI creative technologist with interactive 3D project cards and a dark glassmorphic UI...",
      hint: "<strong>Website Tip:</strong> Mention target audience, required sections (Hero, Showcase, CTA), color palette, responsiveness, and interactive state transitions."
    },
    code: {
      label: "Coding & Software",
      icon: "💻",
      placeholder: "e.g. A high-performance Python rate-limiter using token bucket algorithm with thread safety and Redis fallback...",
      hint: "<strong>Coding Tip:</strong> State programming language, architecture pattern, edge cases, error handling, clean code standards, and unit test suite."
    },
    study: {
      label: "Study & Learning",
      icon: "📚",
      placeholder: "e.g. Explain how neural network backpropagation works using the chain rule and intuitive real-world analogies...",
      hint: "<strong>Study Tip:</strong> Request intuitive ELI5 analogies, first principles breakdown, common pitfalls to avoid, and revision quiz questions."
    },
    writing: {
      label: "Writing & Presentation",
      icon: "✍️",
      placeholder: "e.g. A compelling 5-minute presentation script on how generative AI is transforming modern education...",
      hint: "<strong>Writing Tip:</strong> Specify tone, target audience, structural hook, slide-by-slide outline, and an inspiring call-to-action."
    },
    custom: {
      label: "Custom Meta-Prompt",
      icon: "⚙️",
      placeholder: "e.g. Act as a senior technical consultant and evaluate whether a startup should migrate from monolith to microservices...",
      hint: "<strong>Custom Tip:</strong> Define Persona, Primary Objective, Domain Context, Strict Negative Rules, and Acceptance Criteria."
    }
  };

  // -------------------------------------------------------------------------
  // CATEGORY SWITCHING
  // -------------------------------------------------------------------------
  function setCategory(categoryKey) {
    if (!CATEGORY_META[categoryKey]) categoryKey = 'image';
    
    selectedCategoryInput.value = categoryKey;
    const meta = CATEGORY_META[categoryKey];
    
    // Update active card styling
    categoryCards.forEach(card => {
      const isMatch = card.getAttribute('data-category') === categoryKey;
      card.classList.toggle('active', isMatch);
      card.setAttribute('aria-checked', isMatch ? 'true' : 'false');
    });

    // Update displays
    activeCategoryDisplay.textContent = `Selected: ${meta.label}`;
    categoryHintText.innerHTML = meta.hint;
    ideaInput.setAttribute('placeholder', meta.placeholder);
  }

  categoryCards.forEach(card => {
    card.addEventListener('click', () => {
      const cat = card.getAttribute('data-category');
      setCategory(cat);
    });
  });

  // -------------------------------------------------------------------------
  // STYLE SELECTION
  // -------------------------------------------------------------------------
  styleRadios.forEach(radio => {
    radio.addEventListener('change', (e) => {
      const styleName = e.target.value;
      const formatted = styleName.charAt(0).toUpperCase() + styleName.slice(1);
      activeStyleDisplay.textContent = formatted;
      
      // Update chip styles
      document.querySelectorAll('.style-chip').forEach(chip => {
        const input = chip.querySelector('input');
        chip.classList.toggle('active', input && input.checked);
      });
    });
  });

  // -------------------------------------------------------------------------
  // CHARACTER COUNTERS & INPUT EVENTS
  // -------------------------------------------------------------------------
  function updateCharCount(inputEl, counterEl, max) {
    const len = inputEl.value.length;
    counterEl.textContent = `${len} / ${max}`;
  }

  ideaInput.addEventListener('input', () => {
    updateCharCount(ideaInput, ideaCharCount, 3000);
    if (ideaInput.value.trim().length > 0) {
      ideaErrorMsg.classList.remove('visible');
      ideaInput.style.borderColor = '';
    }
  });

  if (instructionsInput) {
    instructionsInput.addEventListener('input', () => {
      updateCharCount(instructionsInput, instructionsCharCount, 2000);
    });
  }

  clearIdeaBtn.addEventListener('click', () => {
    ideaInput.value = '';
    updateCharCount(ideaInput, ideaCharCount, 3000);
    ideaInput.focus();
  });

  // -------------------------------------------------------------------------
  // TOAST NOTIFICATION UTILITY
  // -------------------------------------------------------------------------
  let toastTimer = null;
  function showToast(message, isError = false) {
    if (toastTimer) clearTimeout(toastTimer);
    toastMessage.textContent = message;
    
    if (isError) {
      toast.style.borderColor = 'var(--danger)';
      toast.querySelector('.toast-icon').style.background = 'var(--danger)';
      toast.querySelector('.toast-icon').textContent = '!';
    } else {
      toast.style.borderColor = 'var(--accent-cyan)';
      toast.querySelector('.toast-icon').style.background = 'var(--accent-cyan)';
      toast.querySelector('.toast-icon').textContent = '✓';
    }

    toast.classList.add('visible');
    toastTimer = setTimeout(() => {
      toast.classList.remove('visible');
    }, 3200);
  }

  // -------------------------------------------------------------------------
  // GENERATE PROMPT (API CALL)
  // -------------------------------------------------------------------------
  async function handleGenerate(isRegeneration = false) {
    if (isSubmitting) return;

    const ideaText = ideaInput.value.trim();
    if (!ideaText) {
      ideaErrorMsg.classList.add('visible');
      ideaInput.style.borderColor = 'var(--danger)';
      ideaInput.focus();
      showToast('Please describe what you want to create first.', true);
      return;
    }

    const category = selectedCategoryInput.value || 'image';
    const selectedStyleRadio = document.querySelector('input[name="style"]:checked');
    const style = selectedStyleRadio ? selectedStyleRadio.value : 'futuristic';
    const instructions = instructionsInput ? instructionsInput.value.trim() : '';

    if (isRegeneration) {
      currentVariation += 1;
    } else {
      currentVariation = 0;
    }

    // Set UI loading state
    isSubmitting = true;
    generateBtn.disabled = true;
    generateBtn.classList.add('loading');
    btnTextContent.innerHTML = 'Crafting Structured Prompt...';

    try {
      const response = await fetch('/api/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          category: category,
          idea: ideaText,
          style: style,
          instructions: instructions,
          variation: currentVariation
        })
      });

      const result = await response.json();

      if (!response.ok || result.status !== 'success') {
        throw new Error(result.message || 'Error occurred while generating prompt.');
      }

      displayResult(result.data);

    } catch (err) {
      console.error('Generation Error:', err);
      showToast(err.message || 'Failed to connect to the server. Please verify Flask is running.', true);
    } finally {
      isSubmitting = false;
      generateBtn.disabled = false;
      generateBtn.classList.remove('loading');
      btnTextContent.innerHTML = `
        <svg class="btn-icon" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"/>
        </svg>
        Generate Prompt
      `;
    }
  }

  // Bind Submit Events
  generatorForm.addEventListener('submit', (e) => {
    e.preventDefault();
    handleGenerate(false);
  });

  generateBtn.addEventListener('click', (e) => {
    e.preventDefault();
    handleGenerate(false);
  });

  regenerateBtn.addEventListener('click', () => {
    handleGenerate(true);
  });

  // -------------------------------------------------------------------------
  // RENDER GENERATED RESULT
  // -------------------------------------------------------------------------
  function displayResult(data) {
    const meta = CATEGORY_META[data.category] || CATEGORY_META.custom;
    
    outputCategoryBadge.textContent = `${meta.icon} ${data.category_label}`;
    outputStyleBadge.textContent = `${data.style_label}`;
    
    // Word count calculation
    const words = data.generated_prompt.trim().split(/\s+/).length;
    outputWordCount.textContent = `${words} Words`;

    outputOriginalIdea.textContent = `"${data.original_idea}"${data.instructions ? ' (Additional: ' + data.instructions + ')' : ''}`;
    promptOutputText.value = data.generated_prompt;

    // Quality Score Rendering
    const q = data.quality;
    if (q) {
      qualityScoreValue.textContent = q.total_score;
      qualityRatingLabel.textContent = q.rating_label;
      qualityProgressFill.style.width = `${q.total_score}%`;

      // Pillars breakdown
      const b = q.breakdown;
      rubricClarity.textContent = `${b.clarity}/25`;
      barClarity.style.width = `${(b.clarity / 25) * 100}%`;

      rubricContext.textContent = `${b.context}/25`;
      barContext.style.width = `${(b.context / 25) * 100}%`;

      rubricSpecificity.textContent = `${b.specificity}/25`;
      barSpecificity.style.width = `${(b.specificity / 25) * 100}%`;

      rubricFormat.textContent = `${b.output_format}/25`;
      barFormat.style.width = `${(b.output_format / 25) * 100}%`;

      // Suggestions
      qualitySuggestionsList.innerHTML = '';
      if (q.suggestions && q.suggestions.length > 0) {
        q.suggestions.forEach(s => {
          const li = document.createElement('li');
          li.textContent = s;
          qualitySuggestionsList.appendChild(li);
        });
      } else {
        const li = document.createElement('li');
        li.textContent = 'Excellent prompt structure! Ready to copy into your AI tool.';
        qualitySuggestionsList.appendChild(li);
      }

      if (q.disclaimer) {
        qualityDisclaimer.textContent = q.disclaimer;
      }
    }

    // Reveal output panel
    outputPanel.classList.remove('hidden');

    // Smooth scroll to output panel
    setTimeout(() => {
      outputPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);

    showToast('Prompt successfully crafted!');
  }

  // -------------------------------------------------------------------------
  // COPY TO CLIPBOARD
  // -------------------------------------------------------------------------
  copyBtn.addEventListener('click', async () => {
    const textToCopy = promptOutputText.value;
    if (!textToCopy) return;

    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(textToCopy);
      } else {
        // Fallback for older browsers or non-https contexts
        promptOutputText.select();
        document.execCommand('copy');
        window.getSelection().removeAllRanges();
      }

      // Visual feedback
      copyText.textContent = 'Copied!';
      copyBtn.style.background = 'linear-gradient(135deg, #10b981 0%, #06b6d4 100%)';
      showToast('Prompt copied to clipboard! Paste into your AI tool.');

      setTimeout(() => {
        copyText.textContent = 'Copy Prompt';
        copyBtn.style.background = '';
      }, 2500);

    } catch (err) {
      console.error('Clipboard copy failed:', err);
      // Last-ditch manual selection
      promptOutputText.focus();
      promptOutputText.select();
      showToast('Please press Ctrl+C (Cmd+C) to copy.', true);
    }
  });

  // -------------------------------------------------------------------------
  // CLEAR OUTPUT
  // -------------------------------------------------------------------------
  clearOutputBtn.addEventListener('click', () => {
    outputPanel.classList.add('hidden');
    currentVariation = 0;
    showToast('Output cleared.');
  });

  // -------------------------------------------------------------------------
  // QUICK EXAMPLES CLICK HANDLER
  // -------------------------------------------------------------------------
  exampleLoadButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const cat = btn.getAttribute('data-category');
      const style = btn.getAttribute('data-style');
      const idea = btn.getAttribute('data-idea');
      const instructions = btn.getAttribute('data-instructions');

      // Set category
      setCategory(cat);

      // Set style
      const targetRadio = document.querySelector(`input[name="style"][value="${style}"]`);
      if (targetRadio) {
        targetRadio.checked = true;
        targetRadio.dispatchEvent(new Event('change'));
      }

      // Set idea
      ideaInput.value = idea;
      updateCharCount(ideaInput, ideaCharCount, 3000);
      ideaErrorMsg.classList.remove('visible');

      // Set instructions
      if (instructionsInput) {
        instructionsInput.value = instructions || '';
        updateCharCount(instructionsInput, instructionsCharCount, 2000);
        if (instructions && instructionsAccordion) {
          instructionsAccordion.open = true;
        }
      }

      // Smooth scroll to generator
      const studioCard = document.querySelector('.studio-card');
      studioCard.scrollIntoView({ behavior: 'smooth', block: 'center' });

      // Highlight pulse
      studioCard.classList.remove('highlight-pulse');
      void studioCard.offsetWidth; // trigger reflow
      studioCard.classList.add('highlight-pulse');

      showToast(`Loaded example into studio! Click "Generate Prompt" when ready.`);
    });
  });

  // Clicking anywhere on example card loads it too
  document.querySelectorAll('.example-card').forEach(card => {
    card.addEventListener('click', (e) => {
      if (e.target.closest('.btn-example-load')) return;
      const loadBtn = card.querySelector('.btn-example-load');
      if (loadBtn) loadBtn.click();
    });
  });

  // -------------------------------------------------------------------------
  // MOBILE NAVIGATION MENU
  // -------------------------------------------------------------------------
  if (mobileToggle && navLinks) {
    mobileToggle.addEventListener('click', () => {
      navLinks.classList.toggle('mobile-open');
    });

    // Close on link click
    navLinks.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        navLinks.classList.remove('mobile-open');
      });
    });
  }

  // Initial character counts
  updateCharCount(ideaInput, ideaCharCount, 3000);
  if (instructionsInput) {
    updateCharCount(instructionsInput, instructionsCharCount, 2000);
  }
});
