class CONFIGS(object):
	def __init__(self):
		# RECORD_THRES
		self.RECORD_START_THRES = 80000000
		self.RECORD_END_THRES = 40000000  # 默认值，具体数值初始化由环境确定
		
		# FSM
		self.FSM = 0  # 初始状态，用于调试
		
		# OCR_THRES
		self.OCR_THRES = 0.001
		
		# STR_SIM_THRES
		self.STR_SIM_THRES = 0.01
		
		# SPEAKER_VERIFICATION_CONFIGS
		self.MODEL_PATH = "./data/models/model.pth"
		self.INPUT_SHAPE = (1, 257, 257)
		self.ORDER_THRESHOLD = 0.4
		self.INPUT_THRESHOLD = 0.3
