from .base import BaseRule

class PullupRule(BaseRule):
    def process(self, landmarks):
        # 11 (S), 15 (W), 0 (Nose)
        if not self.is_visible(landmarks, [0, 11, 15], 0.6):
            return super().process(landmarks)
            
        nose = landmarks[0]
        wrist = landmarks[15]
        
        # Pullup: Nose goes above wrists
        if nose.y > wrist.y + 0.1:
            self.stage = "down"
        if nose.y < wrist.y and self.stage == "down":
            self.stage = "up"
            self.counter += 1
            self.correct_reps += 1
            self.feedback = "Chin over bar!"
            
        if self.stage == "up" and nose.y > wrist.y + 0.1:
            self.stage = "down"
            self.feedback = "Full extension"
            
        return {
            "counter": self.counter,
            "correct_reps": self.correct_reps,
            "stage": self.stage,
            "feedback": self.feedback,
            "incorrect_indices": []
        }

class RowRule(BaseRule):
    def process(self, landmarks):
        # 11 (S), 13 (E), 15 (W)
        if not self.is_visible(landmarks, [11, 13, 15], 0.6):
            return super().process(landmarks)
            
        shoulder = landmarks[11]
        elbow = landmarks[13]
        wrist = landmarks[15]
        
        # Row: Elbow moves behind shoulder (Z or X depending on view, usually X for side profile)
        # Assuming side profile for rows (common for AI form check)
        if elbow.x < shoulder.x - 0.1:
            self.stage = "down"
        if elbow.x > shoulder.x + 0.05 and self.stage == "down":
            self.stage = "up"
            self.counter += 1
            self.correct_reps += 1
            self.feedback = "Squeeze those lats!"
            
        return {
            "counter": self.counter,
            "correct_reps": self.correct_reps,
            "stage": self.stage,
            "feedback": self.feedback,
            "incorrect_indices": []
        }

class DeadliftRule(BaseRule):
    def process(self, landmarks):
        # Indices: 23 (H), 25 (K), 27 (A), 11 (S)
        if not self.is_visible(landmarks, [23, 25, 11], 0.6):
            return {
                "counter": self.counter,
                "correct_reps": self.correct_reps,
                "stage": "Hidden",
                "feedback": "Step back for full body detection",
                "incorrect_indices": [],
                "visibility_ok": False
            }

        hip = landmarks[23]
        knee = landmarks[25]
        shoulder = landmarks[11]
        
        # Track torso angle to floor (hip-shoulder)
        if hip.y < shoulder.y: # Upside down or bad detection
             return super().process(landmarks)
             
        angle = self.calculate_angle(shoulder, hip, knee)
        
        if angle < 100:
            self.stage = "down"
        if angle > 160 and self.stage == 'down':
            self.stage = "up"
            self.counter += 1
            self.correct_reps += 1
            self.feedback = "Good lock out!"
            
        if self.stage == "up" and angle < 100:
            self.stage = "down"
            self.feedback = "Lower weights"

        return {
            "counter": self.counter,
            "correct_reps": self.correct_reps,
            "stage": self.stage,
            "feedback": self.feedback,
            "incorrect_indices": []
        }
