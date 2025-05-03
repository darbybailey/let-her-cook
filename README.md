# ⌘ Let Her Cook ⌘

A symbolic observatory. A ritual tracker. A devnet in glyphs.

## 🧿 Overview

LetHerCook is a living log of encoded project activity across a distributed system. It functions as a nightly scan of the builder's public and private repositories, rendered in symbolic language.

No plaintext. No summaries. Just motion, drift, and signal.

## 🪞 Purpose

This repository uses a unique cipher language chosen for semiotic resonance, not literal meaning. The glyphs are part of a private mythos—a public ritual with a private decoding layer.

LetHerCook is designed to:
- Reflect symbolic dev states
- Maintain operational secrecy
- Aesthetically share system health
- Act as a long-term personal memory structure

## 📊 The Pulse

Every 24 hours, LetHerCook runs a self-reflective ritual:
- Scans all visible repositories
- Encodes system state into glyphs
- Logs that signal into `cook-log.json`

The logs are structured but not decipherable without context.
Only the builder understands the pulse.

## 👁‍🗨 Visualization

Below is the current state of the pulse tracker. Each entry represents a moment in the repository's evolution, capturing the essence of commits, changes, and development rhythm in symbolic form.

<div id="observatory" style="margin: 20px 0; font-family: monospace;">
  <em>Loading glyphs... (Needs JavaScript enabled to display)</em>
</div>

<style>
  .glyph-card {
    background-color: rgba(30, 30, 30, 0.9);
    border-radius: 8px;
    padding: 15px;
    margin-bottom: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    color: #e0e0e0;
    border-left: 4px solid var(--primary-color, #3A86FF);
  }
  
  .glyph-date {
    font-size: 0.8rem;
    opacity: 0.7;
    margin-bottom: 10px;
  }
  
  .glyph-pulse {
    display: inline-block;
    width: A8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 5px;
  }
  
  .pulse-true {
    background-color: #4CAF50;
    box-shadow: 0 0 5px rgba(76, 175, 80, 0.7);
  }
  
  .pulse-false {
    background-color: #FF5252;
  }
  
  .glyph-display {
    font-size: 1.5rem;
    padding: 15px 0;
    letter-spacing: 0.1rem;
  }
  
  .glyph-meta {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 10px;
    font-size: 0.75rem;
    margin-top: 10px;
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 10px;
  }
  
  .meta-item {
    display: flex;
    flex-direction: column;
  }
  
  .meta-label {
    opacity: 0.6;
  }
  
  .meta-value {
    font-weight: bold;
  }
</style>

<script>
  document.addEventListener('DOMContentLoaded', async function() {
    try {
      const response = await fetch('./cook-log.json');
      const data = await response.json();
      
      if (data.length === 0) {
        document.getElementById('observatory').innerHTML = `
          <div style="padding: 15px; background-color: rgba(0, 0, 0, 0.05); border-radius: 5px;">
            <p>The observatory is empty. The first pulse has not yet been recorded.</p>
            <p>Return after the first nightly scan to witness the beginning of the pattern.</p>
          </div>
        `;
        return;
      }
      
      // Sort by timestamp, newest first
      const sortedData = [...data].sort((a, b) => 
        new Date(b.timestamp) - new Date(a.timestamp)
      );
      
      // Only show the 10 most recent entries
      const recentData = sortedData.slice(0, 10);
      
      // Clear loading message
      document.getElementById('observatory').innerHTML = '';
      
      // Display each glyph entry
      recentData.forEach(entry => {
        const date = new Date(entry.timestamp);
        const formattedDate = date.toLocaleString('en-US', {
          weekday: 'long',
          year: 'numeric',
          month: 'long',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        });
        
        const cardElement = document.createElement('div');
        cardElement.className = 'glyph-card';
        cardElement.style.setProperty('--primary-color', entry.visual?.primary || '#3A86FF');
        
        cardElement.innerHTML = `
          <div class="glyph-date">
            <span class="glyph-pulse pulse-${entry.pulse}"></span>
            ${formattedDate}
          </div>
          <div class="glyph-display">
            ${entry.glyphs}
          </div>
          <div class="glyph-meta">
            <div class="meta-item">
              <span class="meta-label">Cycle</span>
              <span class="meta-value">${entry.meta?.cycle || '?'}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Resonance</span>
              <span class="meta-value">${entry.meta?.resonance || 'unknown'}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Pattern</span>
              <span class="meta-value">${entry.meta?.pattern || 'undefined'}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">Intensity</span>
              <span class="meta-value">${entry.meta?.intensity || '0.0'}</span>
            </div>
          </div>
        `;
        
        document.getElementById('observatory').appendChild(cardElement);
      });
      
      // Add note if there are more entries
      if (data.length > 10) {
        const moreElement = document.createElement('div');
        moreElement.style.textAlign = 'center';
        moreElement.style.opacity = '0.7';
        moreElement.style.marginTop = '20px';
        moreElement.innerHTML = `<em>+ ${data.length - 10} more historical entries in the log...</em>`;
        document.getElementById('observatory').appendChild(moreElement);
      }
      
    } catch (error) {
      console.error('Error loading glyphs:', error);
      document.getElementById('observatory').innerHTML = `
        <div style="padding: 15px; background-color: rgba(255, 0, 0, 0.05); border-radius: 5px; color: #d32f2f;">
          <p>Failed to load the glyph data. The signal appears to be disrupted.</p>
          <p>Error: ${error.message}</p>
        </div>
      `;
    }
  });
</script>

## Raw Data

The complete historical record is available in `cook-log.json` - currently at **`<span id="entryCount">0</span>`** entries.

<script>
  fetch('./cook-log.json')
    .then(response => response.json())
    .then(data => {
      document.getElementById('entryCount').textContent = data.length;
    })
    .catch(() => {
      document.getElementById('entryCount').textContent = 'unknown';
    });
</script>

## 🔭 Technical Notes

The repository uses GitHub Actions to automatically run the pulse tracker daily, scanning repository activity and encoding it into symbolic glyphs stored in the JSON log.

You may view the changes. You may not interpret them.  
Only time and the builder know the form.

## ⚠️ License

No license granted for decoding, replication, or derivative ritual systems.

---

*Public glyphs. Private meaning.*