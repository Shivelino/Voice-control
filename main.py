import pickle as pkl
from tkinter import Tk

from config import *
from src.source0 import *
from src.source1 import *
from src.source2 import *
from src.source3 import *


class PROCESS(object):
	def __init__(self):
		# configs
		self.configs = CONFIGS()
		self.FSM = self.configs.FSM  # FSM
		
		# speaker verification model init
		self.sv_model = torch.jit.load(self.configs.MODEL_PATH)
		self.device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
		self.sv_model.to(self.device)
		self.sv_model.eval()
		self.user_feature = None
	
	def run(self):
		while True:
			if self.FSM == 0:
				print("----------------Init----------------")
				if os.path.exists("./data/user_feature/user_feature.pkl"):
					self.user_feature = pkl.load(open("./data/user_feature/user_feature.pkl", "rb"))
					print("Welcome back!")
					time.sleep(1)
					self.FSM = 1
				else:
					print("Welcome to use this software! Please follow the hint to init this.")
					print("------------------------------------------------------------------")
					time.sleep(1)
					print("Now record 3 seconds of audio for later identification: ")
					time.sleep(0.5)
					record_second("./data/tmp/record/user_init.wav", _record_second=3)  # 录制用来提取声纹特征
					# 用户声纹特征
					self.user_feature = \
						infer(self.sv_model, self.configs.INPUT_SHAPE, self.device, "./data/tmp/record/user_init.wav")[
							0]
					pkl.dump(self.user_feature, open("./data/user_feature/user_feature.pkl", "wb"))
					os.remove("./data/tmp/record/user_init.wav")
					self.FSM = 1
				print("Now record 3 seconds of audio for ambient background sound measurement: ")
				time.sleep(0.5)
				self.configs.RECORD_END_THRES = int(record_second("./data/tmp/record/environment_init.wav")) + 20000000
				self.configs.RECORD_START_THRES = self.configs.RECORD_END_THRES + 20000000
				# print(self.configs.RECORD_START_THRES, self.configs.RECORD_END_THRES)
				os.remove("./data/tmp/record/environment_init.wav")
			elif self.FSM == 1:
				print("----------------Ordering----------------")
				try:
					record_auto("./data/tmp/record/test.wav", start_thres=self.configs.RECORD_START_THRES,
					            end_thres=self.configs.RECORD_END_THRES)
					feature = infer(self.sv_model, self.configs.INPUT_SHAPE, self.device, "./data/tmp/record/test.wav")[
						0]
					dist = np.dot(feature, self.user_feature) / (
							np.linalg.norm(feature) * np.linalg.norm(self.user_feature))
					if dist > self.configs.ORDER_THRESHOLD:  # Speaker verification
						pretreatment("./data/tmp/record/test.wav", "./data/tmp/after_filtering/test.wav")
						os.remove("./data/tmp/record/test.wav")
						sentences = change_to_chr("./data/tmp/after_filtering/test/output/test_000.wav")
						if sentences[0] == "输入文字。":
							self.FSM = 2
						elif sentences[0] == "退出运行。":
							exit()
						else:
							orders = sentences_to_order(sentences)
							for i, order in enumerate(orders):
								act(order, OCR_THRES=self.configs.OCR_THRES, STR_SIM_THRES=self.configs.STR_SIM_THRES)
							self.FSM = 1
				except Exception:
					self.FSM = 1
			elif self.FSM == 2:
				print("----------------Inputting----------------")
				tkb = Tk()
				tkb.withdraw()
				try:
					record_auto("./data/tmp/record/test.wav", start_thres=self.configs.RECORD_START_THRES,
					            end_thres=self.configs.RECORD_END_THRES)
					feature = infer(self.sv_model, self.configs.INPUT_SHAPE, self.device, "./data/tmp/record/test.wav")[
						0]
					dist = np.dot(feature, self.user_feature) / (
							np.linalg.norm(feature) * np.linalg.norm(self.user_feature))
					if dist > self.configs.INPUT_THRESHOLD:  # Speaker verification
						pretreatment("./data/tmp/record/test.wav", "./data/tmp/after_filtering/test.wav")
						os.remove("./data/tmp/record/test.wav")
						sentences = change_to_chr("./data/tmp/after_filtering/test/output/test_000.wav")
						if sentences[0] == "退出输入。":
							self.FSM = 1
							tkb.destroy()
						else:
							tkb.clipboard_clear()
							tkb.clipboard_append(sentences[0])
							tkb.update()
							pyautogui.keyDown('ctrl')
							pyautogui.press('v')
							pyautogui.keyUp('ctrl')
							self.FSM = 2
				except Exception:
					self.FSM = 2


if __name__ == "__main__":
	process = PROCESS()
	process.run()
