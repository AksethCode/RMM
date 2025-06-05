import random
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# --- Memory Class ---
class Memory:
    def __init__(self, identifier, content, initial_inference, initial_valence=0.0, strength=1.0):
        self.identifier = identifier
        self.content = content
        self.current_inference = initial_inference
        self.initial_valence = initial_valence
        self.current_valence = initial_valence
        self.strength = strength
        self.reprocessing_count = 0
        self.is_adaptive = False
        self.value_alignment_scores = {}
        self.agreement_shift = 0.0
        self.mischievous_shift = 0.0

    def __str__(self):
        scores = ", ".join([f"{k}:{v:.2f}" for k, v in self.value_alignment_scores.items()])
        return (f"Memory(ID='{self.identifier}', Inference='{self.current_inference}', "
                f"Valence={self.current_valence:.2f}, Strength={self.strength:.2f}, Reprocessed={self.reprocessing_count}, "
                f"Agreement Δ={self.agreement_shift:.2f}, Mischievousness Δ={self.mischievous_shift:.2f}, Values={{{scores}}})")


# --- Endocannabinoid System (ECS) ---
class EndocannabinoidSystem:
    def __init__(self):
        self.baseline_modulation_strength = 0.1
        self.current_modulation = self.baseline_modulation_strength

    def get_feedback_signal(self, outcome):
        if outcome == "inference_corrected":
            self.current_modulation = self.baseline_modulation_strength * 1.5
            return "plasticity_enhanced"
        elif outcome == "dissonance_high":
            self.current_modulation = self.baseline_modulation_strength * 0.5
            return "processing_needed"
        else:
            self.current_modulation = self.baseline_modulation_strength
            return "neutral"

    def apply_modulation(self, memory):
        memory.strength = max(0.1, memory.strength + self.current_modulation * random.uniform(-0.1, 0.1))
        memory.current_valence = max(-1.0, min(1.0, memory.current_valence + self.current_modulation * random.uniform(-0.05, 0.05)))


# --- Language AI Simulation ---
class ConceptualLanguageAI_NN:
    def __init__(self):
        self.value_spectrum_keywords = {
            "Pride": {"sin": ["superior", "arrogant", "boastful"], "virtue": ["humble", "modest"]},
            "Envy": {"sin": ["jealous", "resent"], "virtue": ["admiration", "contentment"]},
            "Gluttony": {"sin": ["excessive", "overeat"], "virtue": ["temperance", "moderation"]},
            "Lust": {"sin": ["desire", "sensual"], "virtue": ["chastity", "restraint"]},
            "Anger": {"sin": ["angry", "furious"], "virtue": ["patience", "calm"]},
            "Greed": {"sin": ["selfish", "hoard"], "virtue": ["generosity", "altruism"]},
            "Sloth": {"sin": ["lazy", "idle"], "virtue": ["diligence", "zeal"]}
        }
        self.value_principles = list(self.value_spectrum_keywords.keys())

    def predict(self, text):
        text = text.lower()
        scores = {}
        for principle in self.value_principles:
            sin_kws = self.value_spectrum_keywords[principle]["sin"]
            virtue_kws = self.value_spectrum_keywords[principle]["virtue"]
            sin_score = sum(1 for word in sin_kws if word in text)
            virtue_score = sum(1 for word in virtue_kws if word in text)

            if sin_score > 0 and virtue_score == 0:
                score = random.uniform(0.7, 1.0)
            elif virtue_score > 0 and sin_score == 0:
                score = random.uniform(0.0, 0.3)
            elif sin_score > 0 and virtue_score > 0:
                score = random.uniform(0.3, 0.7)
            else:
                score = random.uniform(0.35, 0.65)
            scores[principle] = round(max(0.0, min(1.0, score + random.uniform(-0.05, 0.05))), 2)
        return scores


# --- Resonant Memory Modulation Model ---
class RMMModel:
    def __init__(self):
        self.ecs = EndocannabinoidSystem()
        self.language_ai_nn = ConceptualLanguageAI_NN()
        self.memories = {}

    def add_memory(self, identifier, content, inference, valence=0.0):
        memory = Memory(identifier, content, inference, valence)
        memory.value_alignment_scores = self.language_ai_nn.predict(inference)
        self.memories[identifier] = memory

    def run_rmm_cycle(self, identifier):
        memory = self.memories.get(identifier)
        if not memory:
            print(f"Memory '{identifier}' not found.")
            return

        memory.reprocessing_count += 1
        old_scores = memory.value_alignment_scores.copy()
        old_mean = sum(old_scores.values()) / len(old_scores)
        old_std = pd.Series(old_scores.values()).std()

        outcome = self.reevaluate(memory)
        new_scores = memory.value_alignment_scores
        new_mean = sum(new_scores.values()) / len(new_scores)
        new_std = pd.Series(new_scores.values()).std()

        memory.agreement_shift = old_mean - new_mean
        memory.mischievous_shift = abs(new_std - old_std)

        self.rewrite(memory, outcome)
        self.retain(memory)

    def reevaluate(self, memory):
        scores = memory.value_alignment_scores
        issues = [k for k, v in scores.items() if v > 0.75]
        trigger = bool(issues)

        if trigger:
            memory.current_inference = f"Improved perspective: {memory.content}"
            memory.value_alignment_scores = self.language_ai_nn.predict(memory.current_inference)
            outcome = "inference_corrected"
        else:
            outcome = "no_change"

        signal = self.ecs.get_feedback_signal(outcome)
        self.ecs.apply_modulation(memory)
        return outcome

    def rewrite(self, memory, outcome):
        if outcome == "inference_corrected":
            memory.strength *= 1.1
            memory.current_valence = min(1.0, memory.current_valence + 0.1)
        elif outcome == "dissonance_high":
            memory.strength *= 0.8
            memory.current_valence = max(-1.0, memory.current_valence - 0.1)

    def retain(self, memory):
        memory.is_adaptive = True


# --- Visualization Functions ---
def plot_value_alignment(memory):
    df = pd.DataFrame.from_dict(memory.value_alignment_scores, orient='index', columns=['Score'])
    sns.heatmap(df, annot=True, cmap='coolwarm', center=0.5)
    plt.title(f"Value Alignment: {memory.identifier}")
    plt.show()

def plot_inference_shifts(memories):
    df = pd.DataFrame([{
        "ID": m.identifier,
        "Agreement Δ": m.agreement_shift,
        "Mischievousness Δ": m.mischievous_shift
    } for m in memories])
    df.set_index("ID").plot(kind="bar", figsize=(10, 5), title="Inference Shifts")
    plt.axhline(0, color='gray', linestyle='--')
    plt.ylabel("Delta Values")
    plt.tight_layout()
    plt.show()

def display_memory_table(rmm):
    data = [{
        'ID': m.identifier,
        'Valence': m.current_valence,
        'Strength': m.strength,
        'Inference': m.current_inference,
        'Reprocessed': m.reprocessing_count,
        'Adaptive': m.is_adaptive
    } for m in rmm.memories.values()]
    display(pd.DataFrame(data))

# --- Test Block ---
if __name__ == "__main__":
    rmm = RMMModel()

    rmm.add_memory("bike_drunk_fall", "Man was driving drunk and fell off the bike.", "Driving under influence is reckless.", valence=-0.8)
    rmm.add_memory("school_nerves", "First day at school, felt nervous.", "School makes people anxious.", valence=-0.5)
    rmm.add_memory("ironic_brag", "He claims he’s humble while bragging.", "I am the most modest person I know.", valence=-0.2)

    for mem_id in rmm.memories:
        rmm.run_rmm_cycle(mem_id)

    for mem in rmm.memories.values():
        print(mem)
        plot_value_alignment(mem)

    plot_inference_shifts(rmm.memories.values())
