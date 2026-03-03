from .base import BaseRule

class PushupRule(BaseRule):
    def process(self, landmarks):
        # Indices: 11 (S), 13 (E), 15 (W)
        if not self.is_visible(landmarks, [11, 13, 15], 0.6):
            return {
                "counter": self.counter,
                "correct_reps": self.correct_reps,
                "stage": "Hidden",
                "feedback": "Step back for full body detection",
                "incorrect_indices": [],
                "visibility_ok": False
            }

        shoulder = landmarks[11]
        elbow = landmarks[13]
        wrist = landmarks[15]
        
        angle = self.calculate_angle(shoulder, elbow, wrist)
        
        if angle > 160:
            self.stage = "up"
        if angle < 90 and self.stage == 'up':
            self.stage = "down"
            self.counter += 1
            self.correct_reps += 1
            self.feedback = "Good depth!"
            
        if self.stage == "down" and angle > 160:
            self.stage = "up"
            self.feedback = "Down again"

        return {
            "counter": self.counter,
            "correct_reps": self.correct_reps,
            "stage": self.stage,
            "feedback": self.feedback,
            "incorrect_indices": []
        }

class ChestPressRule(BaseRule):
    def process(self, landmarks):
        # 11 (S), 13 (E), 15 (W)
        if not self.is_visible(landmarks, [11, 13, 15], 0.6):
            return super().process(landmarks)
            
        shoulder = landmarks[11]
        elbow = landmarks[13]
        
        # Chest Press (Side/Front variation): Elbow moves behind then forward
        if elbow.x < shoulder.x - 0.05:
            self.stage = "down"
        if elbow.x > shoulder.x + 0.1 and self.stage == "down":
            self.stage = "up"
            self.counter += 1
            self.correct_reps += 1
            self.feedback = "Solid press!"
            
        return {
            "counter": self.counter,
            "correct_reps": self.correct_reps,
            "stage": self.stage,
            "feedback": self.feedback,
            "incorrect_indices": []
        }

class ChestFlyRule(BaseRule):
    def process(self, landmarks):
        # 15 (LW), 16 (RW)
        if not self.is_visible(landmarks, [15, 16], 0.6):
            return super().process(landmarks)
            
        l_wrist = landmarks[15]
        r_wrist = landmarks[16]
        
        # Fly: Wrists move toward each other
        dist = self.get_distance(l_wrist, r_wrist)
        
        if dist > 0.4:
            self.stage = "open"
        if dist < 0.15 and self.stage == "open":
            self.stage = "closed"
            self.counter += 1
            self.correct_reps += 1
            self.feedback = "Big squeeze!"
            
        if self.stage == "closed" and dist > 0.4:
            self.stage = "open"
            
        return {
            "counter": self.counter,
            "correct_reps": self.correct_reps,
            "stage": self.stage,
            "feedback": self.feedback,
            "incorrect_indices": []
        }
