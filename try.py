# def dispaly_detected_frames(confidence, model, st_frame, image):
#     global alarm_on

#     # placeholder to show/hide alert dynamically
#     alert_placeholder = st.empty()

#     image = cv2.resize(image, (720, int(720 * (9 / 16))))
#     result = model.predict(image, conf=confidence)
#     boxes = result[0].boxes

#     # Display detection frame
#     res_plotted = result[0].plot()
#     st_frame.image(
#         res_plotted, caption="Detected Video", channels="BGR", width="content"
#     )

#     detected_state = None  # track current state

#     # If detections found, check class names
#     if boxes is not None:
#         for box in boxes:
#             cls_id = int(box.cls[0])
#             class_name = result[0].names[cls_id]

#             if class_name == "drowsy":
#                 detected_state = "drowsy"
#             elif class_name == "phone":
#                 detected_state = "phone"
#             elif class_name in ["distracted", "head drop", "smoking", "yawn"]:
#                 detected_state = "distracted"

#             # # 🔔 Trigger alarm when class = "drowsy"
#             # if class_name.lower() == "drowsy":
#             #     if not alarm_on:
#             #         alarm_on = True
#             #         threading.Thread(target=play_alarm).start()
#             #         st.warning("⚠️ DROWSINESS DETECTED!")
#             # elif class_name.lower() == "phone":
#             #     if not alarm_on:
#             #         alarm_on = True
#             #         threading.Thread(target=play_alarm).start()
#             #         st.warning("⚠️ PHONE DETECTED!")
#             # elif class_name.lower() in [
#             #     "distracted",
#             #     "head drop",
#             #     "smoking",
#             #     "yawn",
#             # ]:
#             #     if not alarm_on:
#             #         alarm_on = True
#             #         threading.Thread(target=play_alarm).start()
#             #         st.warning("⚠️ DRIVER DISTRACTED!")
#             # else:
#             #     alarm_on = False
#             #     pygame.mixer.music.stop()
#     # 🔔 Manage alarm and message based on detected state
#     if detected_state:
#         if not alarm_on:
#             alarm_on = True
#             threading.Thread(target=play_alarm).start()

#         if detected_state == "drowsy":
#             alert_placeholder.warning("⚠️ DROWSINESS DETECTED!")
#         elif detected_state == "phone":
#             alert_placeholder.warning("⚠️ PHONE DETECTED!")
#         elif detected_state == "distracted":
#             alert_placeholder.warning("⚠️ DRIVER DISTRACTED!")
#     else:
#         # No detection — stop alarm and clear message
#         if alarm_on:
#             pygame.mixer.music.stop()
#             alarm_on = False
#         alert_placeholder.empty()


# def dispaly_detected_frames(confidence, model, st_frame, image):
#     global alarm_on

#     # Placeholders: alert above, frame below
#     if "alert_placeholder" not in st.session_state:
#         st.session_state.alert_placeholder = st.empty()
#     if "video_placeholder" not in st.session_state:
#         st.session_state.video_placeholder = st.empty()

#     # Resize frame and predict
#     image = cv2.resize(image, (720, int(720 * (9 / 16))))
#     result = model.predict(image, conf=confidence)
#     boxes = result[0].boxes

#     # Display video frame
#     res_plotted = result[0].plot()
#     st.session_state.video_placeholder.image(
#         res_plotted, caption="Detected Video", channels="BGR", width="content"
#     )

#     detected_state = None

#     # Identify driver state
#     if boxes is not None and len(boxes) > 0:
#         for box in boxes:
#             cls_id = int(box.cls[0])
#             class_name = result[0].names[cls_id].lower()

#             if class_name == "drowsy":
#                 detected_state = "drowsy"
#                 break
#             elif class_name == "phone":
#                 detected_state = "phone"
#                 break
#             elif class_name in ["distracted", "head drop", "smoking", "yawn"]:
#                 detected_state = "distracted"
#                 break

#     # 🔔 Manage alarm + top alert banner
#     if detected_state:
#         if not alarm_on:
#             alarm_on = True
#             threading.Thread(target=play_alarm, daemon=True).start()

#         # Custom red alert banner styles
#         if detected_state == "drowsy":
#             msg = "⚠️ DROWSINESS DETECTED!"
#         elif detected_state == "phone":
#             msg = "⚠️ PHONE DETECTED!"
#         elif detected_state == "distracted":
#             msg = "⚠️ DRIVER DISTRACTED!"
#         else:
#             msg = ""

#         if msg:
#             st.session_state.alert_placeholder.markdown(
#                 f"""
#                 <div style='background-color:#ff4d4d;
#                             padding:15px;
#                             border-radius:10px;
#                             text-align:center;
#                             color:white;
#                             font-weight:bold;
#                             font-size:18px;
#                             box-shadow:0px 2px 8px rgba(0,0,0,0.2);'>
#                     {msg}
#                 </div>
#                 """,
#                 unsafe_allow_html=True,
#             )
#     else:
#         # Stop alarm and clear alert when normal
#         if alarm_on:
#             pygame.mixer.music.stop()
#             alarm_on = False
#         st.session_state.alert_placeholder.empty()
