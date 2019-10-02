from awc_site.MCDM_code.Malware_Manager import Malware_App_Manager
import tensorflow as tf
tf.keras.backend.clear_session()


graph = tf.get_default_graph()
malware_manager = Malware_App_Manager()