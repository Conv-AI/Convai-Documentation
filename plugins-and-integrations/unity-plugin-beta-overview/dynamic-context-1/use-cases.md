---
description: >-
  Explore practical use cases for Dynamic Context and learn how it improves
  character responsiveness, relevance, and contextual awareness in
  conversations.
---

# Use Cases

## Beginner

### Personalizing the Conversation

The most common use: telling the character who it is speaking with before any dialogue begins.

**Scenario:** The player creates a character and enters the world. The NPC should greet them by name and acknowledge their class.

```csharp
using System.Collections;
using System.Linq;
using Convai.Scripts;
using UnityEngine;

/// <summary>
/// Injects player identity into the active Convai session at session start.
/// The character receives this context before the first exchange and can
/// greet the player by name and class without any dashboard reconfiguration.
/// </summary>
public class PlayerGreeting : MonoBehaviour
{
    [SerializeField] private string _playerName = "Aria";
    [SerializeField] private string _playerClass = "Ranger";

    private ConvaiRoomManager _roomManager;

    private IEnumerator Start()
    {
        while (ConvaiRoomManager.Instance == null)
            yield return null;

        _roomManager = ConvaiRoomManager.Instance;

        while (!_roomManager.IsConnectedToRoom)
            yield return null;

        // runLlm: "true" triggers an immediate character response.
        // The full audio pipeline must be ready before sending — waiting for
        // IsConnectedToRoom alone is not sufficient. The bot participant joins,
        // publishes its audio track, and the AudioStream is initialised
        // asynchronously after the room connects. Sending before all three
        // stages complete causes the TTS response to be silently dropped.
        while (_roomManager.NpcToParticipantMap == null ||
               !_roomManager.NpcToParticipantMap.Values.Any(d => d.AudioStream != null))
        {
            yield return null;
        }

        SendGreeting();
    }

    private void SendGreeting()
    {
        string context =
            $"You are speaking with {_playerName}, a level 1 {_playerClass}. " +
            "Greet them warmly and welcome them to the world.";

        // replace — ensures no stale context from a previous session carries over.
        // runLlm: true — triggers an immediate greeting response.
        bool sent = _roomManager.UpdateDynamicContext(context, mode: "replace", runLlm: "true");
        if (!sent)
            Debug.LogWarning("[PlayerGreeting] UpdateDynamicContext returned false.");
    }
}
```

`replace` ensures no stale context from a previous session carries over. `runLlm: "true"` triggers an immediate greeting response.

***

### Injecting the Learner Profile

At session start, push the learner's name, role, and current course. Every character in the session is immediately personalized without any dashboard reconfiguration.

```csharp
using System.Collections;
using Convai.Scripts;
using UnityEngine;

/// <summary>
/// Injects the active learner's profile into the Convai session at session start.
/// Personalizes every character in the session without dashboard reconfiguration.
/// </summary>
public class LearnerProfileInjector : MonoBehaviour
{
    private ConvaiRoomManager _roomManager;

    private IEnumerator Start()
    {
        while (ConvaiRoomManager.Instance == null)
            yield return null;

        _roomManager = ConvaiRoomManager.Instance;

        if (!_roomManager.IsConnectedToRoom)
        {
            bool connected = false;
            _roomManager.OnRoomConnectionSuccessful.AddListener(() => connected = true);
            yield return new WaitUntil(() => connected);
        }

        InjectProfile();
    }

    private void InjectProfile()
    {
        LearnerProfile profile = LearnerProfileService.Current;
        if (profile == null)
        {
            Debug.LogWarning("[LearnerProfileInjector] No active learner profile found.");
            return;
        }

        string context =
            $"You are speaking with {profile.FullName}, a {profile.JobTitle} " +
            $"in the {profile.Department} department. " +
            $"They are a {profile.ExperienceLevel} learner completing " +
            $"the '{profile.CurrentCourseName}' course. " +
            $"Their stated learning goal: {profile.LearningGoal}. " +
            "Address them by name and calibrate explanations to their experience level.";

        // replace — establishes a clean session baseline.
        // runLlm: false — profile is background context, not a prompt for an immediate response.
        bool sent = _roomManager.UpdateDynamicContext(context, mode: "replace", runLlm: "false");
        if (!sent)
            Debug.LogWarning("[LearnerProfileInjector] UpdateDynamicContext returned false.");
    }
}
```

***

### Module Progression

As the trainee advances to a new module, replace the context with the module's objectives. The character immediately knows what to focus on — no reconfiguration required.

```csharp
using Convai.Scripts;
using UnityEngine;

/// <summary>
/// Updates the character's context whenever the trainee advances to a new training module.
/// The character's focus shifts entirely to the new module — no reconfiguration required.
/// </summary>
public class TrainingModuleController : MonoBehaviour
{
    private ConvaiRoomManager _roomManager;

    /// <summary>
    /// Initializes this component with the active room manager.
    /// Must be called by the session owner after the Convai session is established.
    /// </summary>
    public void Initialize(ConvaiRoomManager roomManager)
    {
        _roomManager = roomManager;
    }

    /// <summary>
    /// Replaces the character's module context with the given module's objectives and concepts.
    /// </summary>
    public void AdvanceToModule(TrainingModule module)
    {
        string context =
            $"The learner is now starting Module {module.Number}: '{module.Title}'. " +
            $"Learning objectives: {string.Join("; ", module.Objectives)}. " +
            $"Key concepts: {string.Join(", ", module.KeyConcepts)}. " +
            $"Estimated duration: {module.EstimatedMinutes} minutes. " +
            "Focus all guidance and questions on this module's content only.";

        // replace — prior module context is no longer relevant.
        bool sent = _roomManager?.UpdateDynamicContext(context, mode: "replace", runLlm: "false") ?? false;
        if (!sent)
            Debug.LogWarning($"[TrainingModuleController] Failed to advance to module '{module.Title}'.");
    }
}
```

***

### Language Tutor Proficiency Level

A language learning tutor adjusts its vocabulary, sentence complexity, and correction style based on the learner's current proficiency level. A single call at session start — or whenever the level changes.

```csharp
using Convai.Scripts;
using UnityEngine;

/// <summary>
/// Sets the language tutor's vocabulary and correction style based on the learner's CEFR level.
/// Call at session start and whenever the level changes (e.g. after a level-up assessment).
/// </summary>
public class LanguageTutorLevelManager : MonoBehaviour
{
    private ConvaiRoomManager _roomManager;

    /// <summary>
    /// Initializes this component with the active room manager.
    /// Must be called by the session owner after the Convai session is established.
    /// </summary>
    public void Initialize(ConvaiRoomManager roomManager)
    {
        _roomManager = roomManager;
    }

    /// <param name="cefrLevel">CEFR proficiency level: A1, A2, B1, B2, C1, or C2.</param>
    /// <param name="nativeLanguage">The learner's native language.</param>
    /// <param name="targetLanguage">The language the learner is studying.</param>
    public void SetProficiencyLevel(string cefrLevel, string nativeLanguage, string targetLanguage)
    {
        string context =
            $"The learner's native language is {nativeLanguage}. " +
            $"They are learning {targetLanguage} at CEFR level {cefrLevel}. " +
            GetLevelInstructions(cefrLevel);

        bool sent = _roomManager?.UpdateDynamicContext(context, mode: "replace", runLlm: "false") ?? false;
        if (!sent)
            Debug.LogWarning($"[LanguageTutorLevelManager] Failed to set proficiency level '{cefrLevel}'.");
    }

    private static string GetLevelInstructions(string level) => level switch
    {
        "A1" or "A2" =>
            "Use only simple present and past tense. Keep sentences under ten words. " +
            "Avoid idioms. Repeat key vocabulary. Correct errors gently by modeling the correct form.",

        "B1" or "B2" =>
            "Use varied sentence structures and introduce common idioms. " +
            "Gently correct grammar errors by rephrasing. Encourage longer responses.",

        "C1" or "C2" =>
            "Speak at natural pace with nuanced vocabulary and idiomatic expressions. " +
            "Correct only significant errors. Engage in abstract or opinion-based discussion.",

        _ => "Adapt to the learner's apparent comprehension level."
    };
}
```

### Injecting Emotional State

Dynamic Context is not limited to facts. Plain-language instructions work equally well for shaping character tone and behavior on the fly.

Scenario: A companion NPC's mood should shift based on what is happening in the scene — calm before a battle, tense during it, relieved after.

```csharp
using Convai.Scripts;
using UnityEngine;

/// <summary>
/// Controls the companion NPC's emotional state and behavioral tone at runtime.
/// Uses plain-language instructions — no separate emotion pipeline required.
/// The new tone surfaces naturally in the next exchange; no immediate response is triggered.
/// </summary>
public class CompanionMoodController : MonoBehaviour
{
    private ConvaiRoomManager _roomManager;

    /// <summary>
    /// Initializes this component with the active room manager.
    /// Must be called by the session owner after the Convai session is established.
    /// </summary>
    public void Initialize(ConvaiRoomManager roomManager)
    {
        _roomManager = roomManager;
    }

    /// <summary>
    /// Replaces the character's current emotional state with the given instruction.
    /// </summary>
    /// <param name="moodInstruction">
    /// A plain-language behavioral instruction.
    /// Example: "You sense danger nearby. Speak with urgency and keep responses short."
    /// </param>
    public void SetMood(string moodInstruction)
    {
        // replace — the current mood replaces the previous one; states do not accumulate.
        // runLlm: false — mood is background context; the character should not react unprompted.
        bool sent = _roomManager?.UpdateDynamicContext(
            moodInstruction,
            mode: "replace",
            runLlm: "false") ?? false;

        if (!sent)
            Debug.LogWarning("[CompanionMoodController] UpdateDynamicContext returned false.");
    }
}

// Usage:
// _moodController.SetMood("You sense danger nearby. Speak with urgency and keep responses short.");
// _moodController.SetMood("The threat has passed. You are relieved but still alert.");
```

`runLlm: "false"` updates the character's disposition silently — the new tone will surface naturally in the next exchange rather than triggering an unsolicited remark.

***

## Intermediate

### Reactive Game State

As the player progresses, the world changes. Dynamic Context lets those changes reach the character in real time.

Scenario: A shopkeeper NPC should always be aware of the player's current gold, recent events, and completed quests.

```csharp
using Convai.Scripts;
using UnityEngine;

/// <summary>
/// Keeps a shopkeeper NPC's context synchronized with the player's real-time game state.
/// Passive state changes (gold, world events) are sent silently.
/// Significant events (quest completions) trigger an immediate character reaction.
/// </summary>
public class ShopkeeperContextUpdater : MonoBehaviour
{
    private ConvaiRoomManager _roomManager;

    private void Awake()
    {
        PlayerInventory.OnGoldChanged += OnGoldChanged;
        QuestManager.OnQuestCompleted += OnQuestCompleted;
        WorldEvents.OnMajorEventOccurred += OnWorldEvent;
    }

    private void OnDestroy()
    {
        PlayerInventory.OnGoldChanged -= OnGoldChanged;
        QuestManager.OnQuestCompleted -= OnQuestCompleted;
        WorldEvents.OnMajorEventOccurred -= OnWorldEvent;
    }

    /// <summary>
    /// Initializes this component and pushes an initial state snapshot.
    /// Must be called by the session owner after the Convai session is established.
    /// </summary>
    public void Initialize(ConvaiRoomManager roomManager)
    {
        if (roomManager == null)
        {
            Debug.LogError("[ShopkeeperContextUpdater] roomManager must not be null.");
            return;
        }

        _roomManager = roomManager;

        // Push initial snapshot — replace any context from a previous session.
        string snapshot =
            $"Player gold: {PlayerInventory.Gold}g. " +
            $"Completed quests: {string.Join(", ", QuestManager.CompletedQuestNames)}. " +
            $"Merchant Guild reputation: {PlayerStats.MerchantReputation}/100.";

        bool sent = _roomManager.UpdateDynamicContext(snapshot, mode: "replace", runLlm: "false");
        if (!sent)
            Debug.LogWarning("[ShopkeeperContextUpdater] Failed to send initial snapshot.");
    }

    private void OnGoldChanged(int newGold)
    {
        // Silent append — gold amount colors future replies without prompting an unsolicited remark.
        bool sent = _roomManager?.UpdateDynamicContext(
            $"Player gold updated: {newGold}g.",
            mode: "append",
            runLlm: "false") ?? false;

        if (!sent)
            Debug.LogWarning("[ShopkeeperContextUpdater] Failed to update gold context.");
    }

    private void OnQuestCompleted(string questName)
    {
        // runLlm: true — the player returning with a completed quest warrants a reaction.
        bool sent = _roomManager?.UpdateDynamicContext(
            $"The player just completed '{questName}' and is returning to collect their reward.",
            mode: "append",
            runLlm: "true") ?? false;

        if (!sent)
            Debug.LogWarning("[ShopkeeperContextUpdater] Failed to send quest completion context.");
    }

    private void OnWorldEvent(string eventDescription)
    {
        // Silent append — world news enriches future conversation without interrupting the current flow.
        bool sent = _roomManager?.UpdateDynamicContext(
            $"World event: {eventDescription}",
            mode: "append",
            runLlm: "false") ?? false;

        if (!sent)
            Debug.LogWarning("[ShopkeeperContextUpdater] Failed to send world event context.");
    }
}
```

Passive state (gold, world news) uses `runLlm: "false"` — it colors future replies without prompting unsolicited comments. Quest completions use `runLlm: "true"` because a reaction is expected.

***

### Silent Event Accumulation

In high-frequency event scenarios — rapid loot drops, kill streaks, bonus triggers — reacting to every event creates noise. The correct pattern is to accumulate silently and respond only when something meaningful happens, or when the user initiates conversation.

Scenario: A combat commentator tracks kill events throughout a fight. The character stays quiet during the action but has full awareness of everything that happened when the player finally speaks.

```csharp
using Convai.Scripts;
using UnityEngine;

/// <summary>
/// Accumulates combat events silently in the character's context.
/// The character stays quiet during the action but has full awareness of everything
/// that happened. It speaks only when a meaningful cluster of events is reached
/// or when a combat phase ends naturally.
/// </summary>
public class CombatEventAccumulator : MonoBehaviour
{
    [SerializeField]
    [Tooltip("Number of events to accumulate before triggering a character response.")]
    private int _responseThreshold = 5;

    private ConvaiRoomManager _roomManager;
    private int _pendingEventCount;

    /// <summary>
    /// Initializes this component with the active room manager.
    /// Must be called by the session owner after the Convai session is established.
    /// </summary>
    public void Initialize(ConvaiRoomManager roomManager)
    {
        if (roomManager == null)
        {
            Debug.LogError("[CombatEventAccumulator] roomManager must not be null.");
            return;
        }
        _roomManager = roomManager;
    }

    /// <summary>
    /// Records a kill event. Accumulates silently until the response threshold is crossed.
    /// </summary>
    public void OnEnemyDefeated(string enemyName, string weaponUsed)
    {
        _pendingEventCount++;

        // Accumulate silently — the character is aware but does not interrupt the action.
        _roomManager?.UpdateDynamicContext(
            $"Player defeated {enemyName} using {weaponUsed}.",
            mode: "append",
            runLlm: "false");

        if (_pendingEventCount < _responseThreshold)
            return;

        // Threshold crossed — a meaningful cluster of events warrants acknowledgment.
        bool sent = _roomManager?.UpdateDynamicContext(
            "The player has been on a significant kill streak. Acknowledge their performance briefly.",
            mode: "append",
            runLlm: "true") ?? false;

        if (!sent)
            Debug.LogWarning("[CombatEventAccumulator] Failed to trigger kill streak response.");

        _pendingEventCount = 0;
    }

    /// <summary>
    /// Flushes any remaining accumulated events at the end of a combat phase.
    /// </summary>
    public void OnCombatPhaseEnded()
    {
        if (_pendingEventCount == 0) return;

        bool sent = _roomManager?.UpdateDynamicContext(
            "Combat phase ended. Summarize what just happened and offer a brief assessment.",
            mode: "append",
            runLlm: "true") ?? false;

        if (!sent)
            Debug.LogWarning("[CombatEventAccumulator] Failed to trigger phase-end response.");

        _pendingEventCount = 0;
    }
}
```

This keeps the character's intervention meaningful. It has full awareness of the event stream but speaks at deliberate moments rather than reacting to every trigger.

***

### Performance-Driven Coaching Difficulty

A sales training simulator tracks the trainee's real-time performance score. When the score shifts enough to cross a difficulty tier, the character's coaching strategy updates mid-session — no restart needed.

```csharp
using Convai.Scripts;
using UnityEngine;

/// <summary>
/// Adapts the AI sales trainer's coaching difficulty in real time based on the
/// trainee's performance score. When the score crosses a tier boundary, the
/// character's strategy updates mid-session — no restart required.
/// </summary>
public class SalesTrainerPerformanceAdapter : MonoBehaviour
{
    [SerializeField] private float _easyThreshold = 75f;
    [SerializeField] private float _hardThreshold = 40f;

    private ConvaiRoomManager _roomManager;
    private string _currentDifficultyTier = "normal";

    /// <summary>
    /// Initializes this component with the active room manager.
    /// Must be called by the session owner after the Convai session is established.
    /// </summary>
    public void Initialize(ConvaiRoomManager roomManager)
    {
        if (roomManager == null)
        {
            Debug.LogError("[SalesTrainerPerformanceAdapter] roomManager must not be null.");
            return;
        }
        _roomManager = roomManager;
    }

    /// <summary>
    /// Evaluates the trainee's current score and updates the coaching strategy
    /// only when the difficulty tier changes or a new skill gap is identified.
    /// </summary>
    /// <param name="newScore">Current performance score (0–100).</param>
    /// <param name="lastMissedSkill">The most recently identified skill gap, or null if none.</param>
    public void OnPerformanceScoreUpdated(float newScore, string lastMissedSkill)
    {
        string newTier = newScore >= _easyThreshold ? "easy"
            : newScore <= _hardThreshold ? "hard"
            : "normal";

        bool tierChanged = newTier != _currentDifficultyTier;
        bool hasNewSkillGap = !string.IsNullOrEmpty(lastMissedSkill);

        // Only push an update when something meaningful has changed.
        if (!tierChanged && !hasNewSkillGap)
            return;

        _currentDifficultyTier = newTier;

        string difficultyInstruction = newTier switch
        {
            "easy" => "The trainee is performing well. Increase objection complexity. Introduce edge cases.",
            "hard" => "The trainee is struggling. Simplify objections. Give conversational hints. Be encouraging.",
            _ => "Maintain current difficulty. Keep objections realistic."
        };

        string context = $"Trainee performance score: {newScore:F0}/100. {difficultyInstruction}";

        if (hasNewSkillGap)
            context += $" The trainee has been missing: {lastMissedSkill}. Subtly probe that area.";

        // replace — the new difficulty state supersedes the previous one entirely.
        bool sent = _roomManager?.UpdateDynamicContext(context, mode: "replace", runLlm: "false") ?? false;
        if (!sent)
            Debug.LogWarning("[SalesTrainerPerformanceAdapter] Failed to update coaching context.");
    }
}
```

***

### Branching Compliance Scenario State

A compliance training simulation where each trainee decision advances a scenario branch. The AI colleague NPC always has full awareness of what decisions were made, their consequences, and the accumulated compliance score.

```csharp
using System.Collections.Generic;
using Convai.Scripts;
using UnityEngine;

/// <summary>
/// Tracks trainee decisions in a branching compliance scenario.
/// The AI colleague NPC always has full awareness of the current scenario branch,
/// accumulated decision history, and compliance score — without reconfiguration
/// between decisions.
/// </summary>
public class ComplianceScenarioTracker : MonoBehaviour
{
    private ConvaiRoomManager _roomManager;
    private readonly List<string> _decisionLog = new();
    private string _currentBranch;
    private int _complianceScore = 100;

    /// <summary>
    /// Initializes this component with the active room manager.
    /// Must be called by the session owner after the Convai session is established.
    /// </summary>
    public void Initialize(ConvaiRoomManager roomManager)
    {
        if (roomManager == null)
        {
            Debug.LogError("[ComplianceScenarioTracker] roomManager must not be null.");
            return;
        }
        _roomManager = roomManager;
    }

    /// <summary>
    /// Records a trainee decision, advances the scenario branch, and pushes the
    /// updated state. Impacts below -20 are treated as critical and trigger an
    /// immediate character reaction.
    /// </summary>
    public void OnTraineeDecision(ScenarioDecision decision)
    {
        _complianceScore += decision.ComplianceImpact;
        _currentBranch = decision.ResultingBranchName;
        _decisionLog.Add($"'{decision.Description}' ({decision.ComplianceImpact:+#;-#;0} pts)");

        bool isError = decision.ComplianceImpact < 0;
        bool isCriticalError = decision.ComplianceImpact < -20;

        string context =
            $"Current scenario branch: {_currentBranch}. " +
            $"Trainee compliance score: {_complianceScore}/100. " +
            $"Decision history: {string.Join(" → ", _decisionLog)}. " +
            $"Last decision consequence: {decision.ConsequenceDescription}. " +
            (isError
                ? "The trainee made a compliance error. Reference it naturally — do not lecture."
                : "The trainee made the correct compliance decision. Acknowledge their judgment.");

        // replace — the full scenario state replaces the previous snapshot on every decision.
        bool sent = _roomManager?.UpdateDynamicContext(
            context,
            mode: "replace",
            runLlm: isCriticalError ? "true" : "false") ?? false;

        if (!sent)
            Debug.LogWarning("[ComplianceScenarioTracker] Failed to update scenario context.");
    }

    /// <summary>
    /// Signals scenario completion and triggers a structured debrief from the character.
    /// </summary>
    public void OnScenarioCompleted()
    {
        string debrief =
            $"The scenario is complete. Final compliance score: {_complianceScore}/100. " +
            $"Provide a brief debrief: acknowledge strengths, identify the most significant error, " +
            $"and give one actionable recommendation. " +
            $"Decision log: {string.Join("; ", _decisionLog)}.";

        bool sent = _roomManager?.UpdateDynamicContext(debrief, mode: "append", runLlm: "true") ?? false;
        if (!sent)
            Debug.LogWarning("[ComplianceScenarioTracker] Failed to send scenario debrief.");
    }
}
```

***

### Medical Simulation Patient Vitals Monitor

A clinical training simulation where a patient NPC's vitals change in real time. The character absorbs routine fluctuations silently but escalates when values cross clinically significant thresholds — without spoiling the diagnosis for the trainee.

```csharp
using System.Collections.Generic;
using Convai.Scripts;
using UnityEngine;

/// <summary>
/// Synchronizes real-time patient vitals with the Convai character context.
/// The character absorbs routine fluctuations silently and escalates only when
/// values cross clinically significant thresholds — without spoiling the diagnosis.
/// </summary>
public class PatientVitalsSimulator : MonoBehaviour
{
    // Clinical thresholds for escalation triggers.
    private const float HypotensionThreshold = 90f;
    private const int BradycardiaThreshold = 50;
    private const float HypoxiaThreshold = 90f;

    private ConvaiRoomManager _roomManager;
    private bool _criticalStateActive;

    /// <summary>
    /// Initializes this component with the active room manager.
    /// Must be called by the session owner after the Convai session is established.
    /// </summary>
    public void Initialize(ConvaiRoomManager roomManager)
    {
        if (roomManager == null)
        {
            Debug.LogError("[PatientVitalsSimulator] roomManager must not be null.");
            return;
        }
        _roomManager = roomManager;
    }

    /// <summary>
    /// Pushes updated patient vitals to the character context.
    /// Triggers an escalation or recovery response when clinical thresholds are crossed.
    /// </summary>
    public void OnVitalsUpdated(PatientVitals vitals)
    {
        // Always update silently — replace, not append (vitals are current state, not a log).
        string vitalsContext =
            $"Current patient vitals — " +
            $"BP: {vitals.SystolicBP}/{vitals.DiastolicBP} mmHg, " +
            $"HR: {vitals.HeartRate} bpm, " +
            $"SpO2: {vitals.OxygenSaturation}%, " +
            $"Temp: {vitals.Temperature:F1}°C, " +
            $"RR: {vitals.RespiratoryRate}/min.";

        _roomManager?.UpdateDynamicContext(vitalsContext, mode: "replace", runLlm: "false");

        bool isCritical =
            vitals.SystolicBP < HypotensionThreshold ||
            vitals.HeartRate < BradycardiaThreshold ||
            vitals.OxygenSaturation < HypoxiaThreshold;

        if (isCritical && !_criticalStateActive)
        {
            _criticalStateActive = true;

            bool sent = _roomManager?.UpdateDynamicContext(
                $"CLINICAL ALERT: {BuildCriticalFindings(vitals)}. " +
                "React as a deteriorating patient. Express distress appropriate to severity. " +
                "Do not tell the trainee what to do — let them diagnose and act.",
                mode: "append",
                runLlm: "true") ?? false;

            if (!sent)
                Debug.LogWarning("[PatientVitalsSimulator] Failed to send critical escalation.");
        }
        else if (!isCritical && _criticalStateActive)
        {
            _criticalStateActive = false;

            bool sent = _roomManager?.UpdateDynamicContext(
                "Patient vitals have stabilized. Express relief. Let the trainee assess next steps.",
                mode: "append",
                runLlm: "true") ?? false;

            if (!sent)
                Debug.LogWarning("[PatientVitalsSimulator] Failed to send stabilization context.");
        }
    }

    private static string BuildCriticalFindings(PatientVitals vitals)
    {
        var findings = new List<string>();

        if (vitals.SystolicBP < HypotensionThreshold)
            findings.Add($"hypotension (BP {vitals.SystolicBP}/{vitals.DiastolicBP})");
        if (vitals.HeartRate < BradycardiaThreshold)
            findings.Add($"bradycardia (HR {vitals.HeartRate} bpm)");
        if (vitals.OxygenSaturation < HypoxiaThreshold)
            findings.Add($"hypoxia (SpO2 {vitals.OxygenSaturation}%)");

        return string.Join(" and ", findings);
    }
}
```

***

## Advanced

### Cross-Scenario Competency Gap Tracker

A multi-scenario training platform tracks which competencies the learner has demonstrated or missed across all scenarios in a session. Each new scenario is informed by the accumulated competency profile so the AI can naturally probe weak areas without the learner being aware of it.

```csharp
using System.Collections.Generic;
using System.Linq;
using Convai.Scripts;
using UnityEngine;

/// <summary>
/// Tracks learner competency observations across multiple training scenarios.
/// Each new scenario is informed by the accumulated competency profile, allowing
/// the AI to naturally probe weak areas without the learner being aware of it.
/// Persists across scene loads via DontDestroyOnLoad.
/// </summary>
public sealed class CompetencyGapTracker : MonoBehaviour
{
    public static CompetencyGapTracker Instance { get; private set; }

    private ConvaiRoomManager _roomManager;
    private readonly Dictionary<string, CompetencyRecord> _competencies = new();

    private void Awake()
    {
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject);
            return;
        }
        Instance = this;
        DontDestroyOnLoad(gameObject);
    }

    /// <summary>
    /// Initializes this tracker with the active room manager.
    /// Must be called by the session owner after the Convai session is established.
    /// </summary>
    public void Initialize(ConvaiRoomManager roomManager)
    {
        if (roomManager == null)
        {
            Debug.LogError("[CompetencyGapTracker] roomManager must not be null.");
            return;
        }
        _roomManager = roomManager;
    }

    /// <summary>
    /// Records a pass or fail observation for a named competency.
    /// Requires at least two observations before a competency influences scenario injection.
    /// </summary>
    /// <param name="competencyId">Stable identifier (e.g. "active-listening").</param>
    /// <param name="competencyName">Human-readable name passed to the character.</param>
    /// <param name="demonstrated">True if the trainee demonstrated this competency.</param>
    public void RecordObservation(string competencyId, string competencyName, bool demonstrated)
    {
        if (!_competencies.TryGetValue(competencyId, out var record))
            record = _competencies[competencyId] = new CompetencyRecord(competencyName);

        record.AddObservation(demonstrated);
    }

    /// <summary>
    /// Pushes accumulated competency intelligence into the next scenario's context.
    /// The character will naturally create opportunities for the trainee to practice gap areas.
    /// </summary>
    public void OnNewScenarioStarted(string scenarioName, string scenarioContext)
    {
        string gaps = BuildGapSummary();
        string strengths = BuildStrengthSummary();

        string context =
            $"New scenario: '{scenarioName}'. {scenarioContext} " +
            $"Trainee strengths from prior scenarios: {strengths}. " +
            $"Competency gaps to probe this scenario: {gaps}. " +
            $"Create natural opportunities to practice gap areas. " +
            "Do not make it obvious you are targeting weaknesses.";

        // replace — each scenario starts with a fresh, scenario-specific context.
        bool sent = _roomManager?.UpdateDynamicContext(context, mode: "replace", runLlm: "false") ?? false;
        if (!sent)
            Debug.LogWarning($"[CompetencyGapTracker] Failed to inject context for scenario '{scenarioName}'.");
    }

    /// <summary>
    /// Triggers a full session debrief based on the complete competency record.
    /// Call when all scenarios in the session are complete.
    /// </summary>
    public void OnSessionCompleted()
    {
        string report = string.Join("; ", _competencies.Values
            .OrderBy(r => r.SuccessRate)
            .Select(r => $"{r.Name}: {r.SuccessRate:P0} ({r.TotalObservations} observations)"));

        bool sent = _roomManager?.UpdateDynamicContext(
            "Training session complete. Deliver a structured debrief: overall performance summary, " +
            "two key strengths, two priority development areas, one concrete next step. " +
            $"Competency data: {report}",
            mode: "replace",
            runLlm: "true") ?? false;

        if (!sent)
            Debug.LogWarning("[CompetencyGapTracker] Failed to trigger session debrief.");
    }

    // Competencies with fewer than two observations are excluded — insufficient data.
    private string BuildGapSummary()
    {
        var gaps = _competencies.Values
            .Where(r => r.TotalObservations >= 2 && r.SuccessRate < 0.6f)
            .Select(r => $"{r.Name} ({r.SuccessRate:P0})")
            .ToList();

        return gaps.Count > 0 ? string.Join(", ", gaps) : "No significant gaps identified yet.";
    }

    private string BuildStrengthSummary()
    {
        var strengths = _competencies.Values
            .Where(r => r.TotalObservations >= 2 && r.SuccessRate >= 0.8f)
            .Select(r => $"{r.Name} ({r.SuccessRate:P0})")
            .ToList();

        return strengths.Count > 0 ? string.Join(", ", strengths) : "Insufficient data.";
    }

    private sealed class CompetencyRecord
    {
        public string Name { get; }
        public int TotalObservations { get; private set; }
        private int _demonstratedCount;

        public float SuccessRate => TotalObservations == 0 ? 0f
            : (float)_demonstratedCount / TotalObservations;

        public CompetencyRecord(string name) => Name = name;

        public void AddObservation(bool demonstrated)
        {
            TotalObservations++;
            if (demonstrated) _demonstratedCount++;
        }
    }
}
```

#### Usage across scenarios:

```csharp
// During a scenario — record what you observe
CompetencyGapTracker.Instance.RecordObservation(
    "active-listening", "Active Listening", demonstrated: true);

CompetencyGapTracker.Instance.RecordObservation(
    "objection-handling", "Objection Handling", demonstrated: false);

// Inject accumulated intelligence before the next scenario
CompetencyGapTracker.Instance.OnNewScenarioStarted(
    "Difficult Customer — Refund Request",
    "The customer is upset about a delayed order and requesting a full refund.");

// At session end — trigger full debrief
CompetencyGapTracker.Instance.OnSessionCompleted();
```

***

### Real-Time Procedural Assessment

A high-fidelity procedural trainer (flight simulator, surgical trainer, industrial safety) monitors every action against a defined checklist. Actions accumulate silently. When the same step fails repeatedly, the AI instructor intervenes with a Socratic question — never giving the answer, but guiding the trainee's thinking.

```csharp
using System.Collections.Generic;
using System.Linq;
using Convai.Scripts;
using UnityEngine;

/// <summary>
/// AI instructor for high-fidelity procedural training simulations
/// (flight, surgical, industrial safety). Monitors every trainee action silently
/// and intervenes with Socratic guidance only when a repeated error pattern is
/// detected — preserving independent problem-solving throughout.
/// </summary>
public class ProceduralAssessmentInstructor : MonoBehaviour
{
    [SerializeField]
    [Tooltip("Number of failures on the same step before a coaching intervention is triggered.")]
    private int _errorPatternThreshold = 2;

    [SerializeField]
    [Tooltip("Minimum seconds between coaching interventions. Prevents rapid-fire interruptions.")]
    private float _interventionCooldownSeconds = 30f;

    private ConvaiRoomManager _roomManager;
    private readonly Dictionary<string, int> _stepErrorCounts = new();
    private readonly List<string> _completedSteps = new();
    private float _lastInterventionTime = float.MinValue;
    private string _currentProcedureName;

    /// <summary>
    /// Initializes this component with the active room manager.
    /// Must be called by the session owner after the Convai session is established.
    /// </summary>
    public void Initialize(ConvaiRoomManager roomManager)
    {
        if (roomManager == null)
        {
            Debug.LogError("[ProceduralAssessmentInstructor] roomManager must not be null.");
            return;
        }
        _roomManager = roomManager;
    }

    /// <summary>
    /// Signals the start of a procedure. Resets all tracking state and instructs
    /// the character to observe silently until intervention is warranted.
    /// </summary>
    public void BeginProcedure(string procedureName)
    {
        _currentProcedureName = procedureName;
        _stepErrorCounts.Clear();
        _completedSteps.Clear();
        _lastInterventionTime = float.MinValue;

        bool sent = _roomManager?.UpdateDynamicContext(
            $"The trainee is beginning the '{procedureName}' procedure. " +
            "Observe silently unless asked for help or a critical error occurs. " +
            "Do not volunteer the next step — the trainee must demonstrate independent recall.",
            mode: "replace",
            runLlm: "false") ?? false;

        if (!sent)
            Debug.LogWarning($"[ProceduralAssessmentInstructor] Failed to begin procedure '{procedureName}'.");
    }

    /// <summary>
    /// Records a step attempt. Correct steps are acknowledged silently.
    /// Repeated failures on the same step trigger a Socratic intervention
    /// once the error threshold is met and the cooldown has elapsed.
    /// </summary>
    public void OnStepAttempted(string stepId, string stepDescription, bool wasCorrect, bool wasInSequence)
    {
        if (wasCorrect && wasInSequence)
        {
            _completedSteps.Add(stepDescription);

            // Silently acknowledge correct progress — no character response needed.
            _roomManager?.UpdateDynamicContext(
                $"Step completed correctly: {stepDescription}. " +
                $"Progress: {_completedSteps.Count} steps done.",
                mode: "append",
                runLlm: "false");

            return;
        }

        _stepErrorCounts.TryGetValue(stepId, out int errorCount);
        _stepErrorCounts[stepId] = ++errorCount;

        // Accumulate the error silently for context grounding.
        _roomManager?.UpdateDynamicContext(
            $"Error on step '{stepDescription}' " +
            $"(error count: {errorCount}, in-sequence: {wasInSequence}).",
            mode: "append",
            runLlm: "false");

        bool patternDetected = errorCount >= _errorPatternThreshold;
        bool cooldownElapsed = Time.realtimeSinceStartup - _lastInterventionTime > _interventionCooldownSeconds;

        if (!patternDetected || !cooldownElapsed)
            return;

        _lastInterventionTime = Time.realtimeSinceStartup;

        // Intervene with a Socratic question — guide thinking without revealing the answer.
        bool sent = _roomManager?.UpdateDynamicContext(
            $"The trainee has failed '{stepDescription}' {errorCount} times. " +
            "Intervene with one Socratic question that guides their thinking without revealing the answer. " +
            "Be calm and constructive.",
            mode: "append",
            runLlm: "true") ?? false;

        if (!sent)
            Debug.LogWarning("[ProceduralAssessmentInstructor] Failed to trigger coaching intervention.");
    }

    /// <summary>
    /// Signals the end of the procedure and triggers a structured debrief from the character.
    /// </summary>
    public void OnProcedureCompleted(bool passed, float elapsedSeconds)
    {
        int totalErrors = _stepErrorCounts.Values.Sum();
        string worstStep = _stepErrorCounts.Count > 0
            ? _stepErrorCounts.OrderByDescending(kv => kv.Value).First().Key
            : "none";

        // replace — the debrief context supersedes all accumulated step-level context.
        bool sent = _roomManager?.UpdateDynamicContext(
            $"Procedure '{_currentProcedureName}' complete. Result: {(passed ? "PASS" : "FAIL")}. " +
            $"Time: {elapsedSeconds:F0}s. Total errors: {totalErrors}. " +
            $"Most problematic step: '{worstStep}' ({_stepErrorCounts.GetValueOrDefault(worstStep, 0)} errors). " +
            "Deliver a one-sentence overall assessment, the single most important error to address, and one thing they did well.",
            mode: "replace",
            runLlm: "true") ?? false;

        if (!sent)
            Debug.LogWarning("[ProceduralAssessmentInstructor] Failed to trigger procedure debrief.");
    }
}
```

**What this pattern enforces:**

* The instructor has full awareness of every action without constantly interrupting — the character is always listening
* The Socratic threshold prevents the instructor from becoming a hint machine — it speaks only when a genuine learning barrier is detected
* The cooldown prevents rapid-fire interventions that would undermine independent thinking
* The final debrief draws on the accumulated event log for a substantive, evidence-based assessment rather than a generic summary

***

### Reactive Character with Autonomous Response Thresholds

The most sophisticated pattern: the character monitors a continuous stream of game state updates and decides autonomously when to speak — without waiting for the user to initiate. This is a reactive architecture. The character is always listening, but only surfaces when something crosses a meaningful threshold.

Scenario: A companion NPC tracks the player's health passively throughout the session, warns at a moderate drop, and urgently intervenes at a critical level — all without any input from the player.

```csharp
using Convai.Scripts;
using UnityEngine;

/// <summary>
/// A companion NPC that monitors game state passively and reacts autonomously
/// when meaningful thresholds are crossed — without waiting for the player to speak.
/// Silent updates keep the character continuously informed; runLlm: true is reserved
/// exclusively for moments that warrant a proactive response.
/// </summary>
public class ReactiveCompanion : MonoBehaviour
{
    [SerializeField]
    [Tooltip("Health percentage at which the companion first expresses concern.")]
    private float _warningThreshold = 50f;

    [SerializeField]
    [Tooltip("Health percentage at which the companion intervenes urgently.")]
    private float _criticalThreshold = 20f;

    private ConvaiRoomManager _roomManager;
    private float _lastHealth = 100f;

    // Flags prevent repeated interventions for the same threshold crossing.
    private bool _warningIssued;
    private bool _criticalIssued;

    /// <summary>
    /// Initializes this component with the active room manager.
    /// Must be called by the session owner after the Convai session is established.
    /// </summary>
    public void Initialize(ConvaiRoomManager roomManager)
    {
        if (roomManager == null)
        {
            Debug.LogError("[ReactiveCompanion] roomManager must not be null.");
            return;
        }
        _roomManager = roomManager;
    }

    /// <summary>
    /// Silently tracks player health and triggers proactive responses at defined thresholds.
    /// </summary>
    public void OnPlayerHealthChanged(float newHealth)
    {
        // Keep the character silently informed — replace, not append (current state, not a log).
        _roomManager?.UpdateDynamicContext(
            $"Player health: {newHealth:F0}%.",
            mode: "replace",
            runLlm: "false");

        // Warn once when crossing the warning threshold downward.
        if (newHealth <= _warningThreshold && _lastHealth > _warningThreshold && !_warningIssued)
        {
            _warningIssued = true;

            bool sent = _roomManager?.UpdateDynamicContext(
                "Player health has dropped below 50%. Express concern and suggest they find cover or heal.",
                mode: "append",
                runLlm: "true") ?? false;

            if (!sent)
                Debug.LogWarning("[ReactiveCompanion] Failed to send health warning.");
        }

        // Critical intervention — triggers once per threshold crossing until health recovers.
        if (newHealth <= _criticalThreshold && !_criticalIssued)
        {
            _criticalIssued = true;

            bool sent = _roomManager?.UpdateDynamicContext(
                "CRITICAL: Player health is dangerously low. React with urgency — tell them to heal immediately.",
                mode: "append",
                runLlm: "true") ?? false;

            if (!sent)
                Debug.LogWarning("[ReactiveCompanion] Failed to send critical health warning.");
        }

        // Reset both flags when health recovers above the warning threshold.
        if (newHealth > _warningThreshold)
        {
            _warningIssued = false;
            _criticalIssued = false;
        }

        _lastHealth = newHealth;
    }

    /// <summary>
    /// Triggers an immediate proactive warning when the player enters a known danger zone.
    /// </summary>
    public void OnPlayerEnteredDangerZone(string zoneName)
    {
        bool sent = _roomManager?.UpdateDynamicContext(
            $"The player has entered {zoneName}, a known danger zone. Proactively warn them.",
            mode: "append",
            runLlm: "true") ?? false;

        if (!sent)
            Debug.LogWarning("[ReactiveCompanion] Failed to send danger zone warning.");
    }

    /// <summary>
    /// Nudges the character to check in naturally after the player has been idle too long.
    /// Only the intent is injected — the LLM determines the specific wording.
    /// </summary>
    public void OnPlayerIdleTooLong()
    {
        bool sent = _roomManager?.UpdateDynamicContext(
            "The player has been idle for an unusually long time. Check in with them naturally.",
            mode: "append",
            runLlm: "true") ?? false;

        if (!sent)
            Debug.LogWarning("[ReactiveCompanion] Failed to send idle check-in.");
    }
}
```

Silent updates via `runLlm: "false"` keep the character's knowledge current at all times. `runLlm: "true"` is reserved exclusively for moments that genuinely warrant a proactive response. The threshold logic ensures the character intervenes once — not repeatedly — until the situation resolves.
