## Airtable Schema for Novel Project (Revised with Granular Tagging)

This document outlines the proposed schema for organizing the novel in Airtable, including detailed meta-tagging based on narrative design and ontology principles to aid in analysis and project management for a proprietary novel generation workflow.

### Base Name: Novel Project (User to Create)

#### Table 1: Chapters

*   **Fields:**
    *   `ChapterID` (Primary Key): Unique identifier (e.g., "CH001", "CH002").
    *   `ChapterNumber` (Number): Numerical order of the chapter (e.g., 1, 2, 3).
    *   `ChapterTitle` (Single line text): Title of the chapter.
    *   `Status` (Single select): Current status of the chapter (e.g., "Draft", "Needs Granular Tagging", "Tagging in Progress", "Tagging Complete", "Uploaded to Airtable", "Needs Expansion", "Revised").
    *   `WordCount` (Number): Total word count of the chapter.
    *   `Synopsis` (Long text): A brief summary of the key events and plot points in the chapter.
    *   `CharactersAppearing` (Link to `Characters` table, multiple records): Characters appearing in this chapter.
    *   `PrimaryThemes` (Link to `Themes` table, multiple records): Key themes addressed in the chapter.
    *   `RevisionNotes` (Long text): Specific notes for revision or expansion for this chapter.
    *   `LinkToSegments` (Link to `TextSegments` table, multiple records): Links to all text segments belonging to this chapter.
    *   `FullText_Original` (Long text, Markdown enabled): The full text of the chapter *before* segmentation. (Consider Airtable cell limits; might need to store as an attachment or link to a file).

#### Table 2: Text Segments (User to Create this Table)

*   **Fields:**
    *   `SegmentID` (Primary Key): Unique identifier for the text segment (e.g., "CH001_SEG00001").
    *   `Chapter` (Link to `Chapters` table, single record): The chapter this segment belongs to.
    *   `SegmentOrder` (Number): Numerical order of the segment within the chapter.
    *   `SegmentText` (Long text): The actual text of the segment.
    *   `PrimaryNarrativeMode` (Single select): Options: "Dialogue", "Narration-Action", "Narration-Exposition", "Narration-Description", "Narration-InteriorState", "CharacterPOV-Direct", "Meta-Narration", "Other".
    *   `SecondaryNarrativeModes` (Multiple select from `PrimaryNarrativeMode` options).
    *   `DialogueSpeaker` (Link to `Characters` table, single record): Applicable if `PrimaryNarrativeMode` is "Dialogue".
    *   `DialogueAddressees` (Link to `Characters` table, multiple records): Applicable if `PrimaryNarrativeMode` is "Dialogue".
    *   `DialogueContext` (Single line text): E.g., "Interrogation", "Planning Session", "Casual Banter", "Argument", "Confession". Applicable if `PrimaryNarrativeMode` is "Dialogue".
    *   `DialogueTone` (Multiple select): Options: "Satirical", "Serious", "Humorous", "Tense", "Emotional", "Informative", "Sarcastic", "Neutral", "Aggressive", "Submissive". Applicable if `PrimaryNarrativeMode` is "Dialogue".
    *   `PlotFunctionTags` (Multiple select): Options: "IncitingIncident", "RisingActionSegment", "ClimaxSegment", "FallingActionSegment", "ResolutionSegment", "TurningPoint", "ObstacleEncountered", "GoalSetting", "PlanMaking", "PlanExecution", "ConflictExternal", "ConflictInternal", "SuspenseBuilding", "Revelation", "PlotTwist", "SubplotDevelopment".
    *   `MysteryTags` (Multiple select): Options: "ClueDeployment", "ClueAnalysisByCharacter", "Foreshadowing", "RedHerring", "Misdirection", "EvidenceGathering", "DeductionByCharacter", "InterrogationSegment", "WitnessTestimony".
    *   `CharacterArcTags` (Multiple select): Options: "CharacterIntroduction", "CharacterDevelopmentMoment", "RelationshipDevelopment", "RelationshipConflict", "MotivationRevealed", "BackstoryExposition", "InternalStruggleDemonstrated", "DecisionPointForCharacter", "CharacterRealization", "CharacterFlawDemonstrated", "CharacterStrengthDemonstrated", "CharacterGoalEstablished", "CharacterGoalProgress".
    *   `WorldBuildingTags` (Multiple select): Options: "SettingDescriptionPhysical", "SettingDescriptionAtmospheric", "LoreExposition", "TechnologyExplanation", "MagicSystemExplanation", "CulturalNormsExplained", "SocietalStructureExplained", "FactionIntroduction", "HistoricalReferenceWithinWorld".
    *   `StructuralOntologyTags` (Multiple select, inspired by `narrative_ontology.py`): "ObjectiveEventDescription", "SubjectiveCharacterAccount", "CausalLink-Catalyst", "CausalLink-Consequence", "KnowledgePrerequisiteEstablished", "TimeMarkerExplicit", "TimeMarkerImplicit", "LocationMarkerExplicit", "LocationMarkerImplicit", "FlashbackMarker", "FlashforwardMarker", "PerspectiveShiftMarker".
    *   `AuthorialIntentTags` (Multiple select, inspired by `narrative_design.md` and general literary analysis): "SatiricalElement", "HumorousElement", "SocialCommentary", "PhilosophicalPoint", "EmotionalAppeal", "PacingControl-Fast", "PacingControl-Slow", "TensionRelease".
    *   `ThematicKeywordsRaw` (Long text): Comma-separated keywords identified in the segment (e.g., "isolation, power, corruption, hope"). To be processed into links to `Themes` table.
    *   `CharactersInSegment` (Link to `Characters` table, multiple records): All characters actively present or significantly mentioned.
    *   `CharacterPOVHolder` (Link to `Characters` table, single record): Applicable if `PrimaryNarrativeMode` is "CharacterPOV-Direct".
    *   `LocationInSegment` (Link to `Locations` table or Single line text): Specific setting of the segment.
    *   `TimeReferenceInSegment` (Single line text): E.g., "Day 1, Morning", "Night", "Next Day", "Several hours later".
    *   `ClueReferenceInSegment` (Link to `Clues` table, multiple records).
    *   `SegmentNotes` (Long text): For manual notes, script-generated confidence scores, or flags for review.

#### Table 3: Characters (User to Create or Link if Exists)

*   **Fields:**
    *   `CharacterName` (Primary Key, Single line text): Full name of the character.
    *   `Role` (Single select): E.g., "Protagonist", "Antagonist", "Major Supporting", "Minor Supporting", "MentionedOnly".
    *   `DescriptionBio` (Long text): Detailed description, background, motivations, key relationships.
    *   `FirstAppearanceChapter` (Link to `Chapters` table, single record).
    *   `KeyTraits` (Multiple select or Long text): Defining personality traits.
    *   `CharacterArcSynopsis` (Long text): Overview of the character's development.
    *   `LinkedSegments` (Link to `TextSegments` table, multiple records, via `CharactersInSegment`, `DialogueSpeaker`, `DialogueAddressees`, `CharacterPOVHolder` fields).

#### Table 4: Clues (User to Create or Link if Exists)

*   **Fields:**
    *   `ClueID` (Primary Key, Single line text or Autonumber).
    *   `ClueDescription` (Long text).
    *   `SignificanceToMystery` (Long text).
    *   `ChapterIntroduced` (Link to `Chapters` table, single record).
    *   `SegmentIntroduced` (Link to `TextSegments` table, single record).
    *   `TypeOfClue` (Single select): E.g., "PhysicalEvidence", "VerbalInformation", "Observation", "DocumentaryEvidence", "DigitalEvidence", "RedHerring".
    *   `InformationRevealedToReaderAt` (Link to `TextSegments` table, single record).
    *   `InformationUnderstoodByProtagonistAt` (Link to `TextSegments` table, single record).
    *   `RelatedCharacters` (Link to `Characters` table, multiple records).
    *   `ClueStatus` (Single select): E.g., "Introduced", "PartiallyUnderstood", "FullyUnderstood", "Misinterpreted", "Resolved".

#### Table 5: Locations (User to Create or Link if Exists)

*   **Fields:**
    *   `LocationName` (Primary Key, Single line text).
    *   `LocationDescription` (Long text).
    *   `SignificanceToPlot` (Long text).
    *   `FirstAppearanceChapter` (Link to `Chapters` table, single record).
    *   `LinkedSegments` (Link to `TextSegments` table, multiple records, via `LocationInSegment` field).

#### Table 6: Themes (User to Create)

*   **Fields:**
    *   `ThemeName` (Primary Key, Single line text): E.g., "Isolation", "The Nature of Good and Evil", "Redemption".
    *   `ThemeDescription` (Long text): Elaboration on the theme.
    *   `LinkedChapters` (Link to `Chapters` table, multiple records, via `PrimaryThemes` field).
    *   `LinkedSegments` (Link to `TextSegments` table, multiple records, via processed `ThematicKeywordsRaw`).

This revised schema provides a highly granular framework. The `segmenter_script.py` will be updated to populate these fields, though initial automated tagging for complex categories will be heuristic and may require manual refinement or more advanced NLP integration later.
