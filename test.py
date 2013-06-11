import unittest
import lucid

class test(unittest.TestCase):
    noLoopsGrp = ["no_loop.png","test_id232.png"]
    robotArmGrp=["no_loop2.png","no_loop3.png","no_loop4.png"]
    horizontalCenteredLoopsGrp = ["loop_center_face2.png","loop_center_profile1.png",
    "loop_center_face.png","loop_center_profile2.png","loop_right_face2.png",
    "loop_right_profile1.png","loop_right_face.png","loop_right_profile2.png",
    "loop_right_face2.png","loop_right_profile1.png","loop_right_face.png","loop_right_profile2.png",
    "badfocus2_center_face.png","badfocus3_center_face.png","badfocus_center_face.png",
    "badfocus2_center_profile.png","badfocus3_center_profile.png","badfocus_center_profile.png",
    "tache_center_face.png","tache_center_profile.png","imagepos/positive_shield88.png","imagepos/positive_02_normal127.png",
    "imagepos/positive_triangle9.png","imagepos/positive_02_normal64.png","imagepos/positive_shield31.png","imagepos/positive_triangle137.png",
    "imagepos/positive_triangle71.png","imagepos/positive_02_normal49.png","imagepos/positive_triangle178.png","imagepos/positive_normal70.png",
    "imagepos/positive_triangle10.png","imagepos/positive_shield10.png","imagepos/positive_02_normal180.png","imagepos/positive_02_normal116.png",
    "imagepos/positive_normal144.png","imagepos/positive_02_normal174.png","imagepos/positive_triangle61.png","imagepos/positive_triangle23.png",
    "imagepos/positive_normal126.png","imagepos/positive_triangle29.png","imagepos/positive_02_normal138.png","imagepos/positive_shield52.png",
    "imagepos/positive_normal33.png","imagepos/positive_normal14.png","imagepos/positive_shield187.png","imagepos/positive_02_normal123.png",
    "imagepos/positive_normal29.png","imagepos/positive_normal60.png","imagepos/positive_triangle69.png","imagepos/positive_normal131.png",
    "imagepos/positive_02_normal83.png","imagepos/positive_triangle66.png","imagepos/positive_normal112.png","imagepos/positive_shield128.png",
    "imagepos/positive_triangle127.png","imagepos/positive_triangle13.png","imagepos/positive_02_normal81.png","imagepos/positive_triangle81.png",
    "imagepos/positive_02_normal86.png","imagepos/positive_shield170.png","imagepos/positive_normal192.png","imagepos/positive_shield182.png",
    "imagepos/positive_normal96.png","imagepos/positive_triangle80.png","imagepos/positive_triangle192.png","imagepos/positive_normal35.png",
    "imagepos/positive_02_normal102.png","imagepos/positive_shield120.png","imagepos/positive_triangle167.png","imagepos/positive_triangle104.png",
    "imagepos/positive_normal94.png","imagepos/positive_02_normal179.png","imagepos/positive_02_normal4.png", "imagepos/positive_02_normal148.png",
    "imagepos/positive_shield150.png","imagepos/positive_normal55.png","imagepos/positive_02_normal19.png","imagepos/positive_02_normal65.png",
    "imagepos/positive_normal26.png","imagepos/positive_triangle99.png","imagepos/positive_triangle181.png","imagepos/positive_shield56.png",
    "imagepos/positive_normal103.png","imagepos/positive_shield116.png","imagepos/positive_triangle116.png","imagepos/positive_02_normal103.png",
    "imagepos/positive_triangle95.png","imagepos/positive_normal154.png","imagepos/positive_shield68.png","imagepos/positive_shield4.png",
    "imagepos/positive_02_normal11.png","imagepos/positive_02_normal0.png","imagepos/positive_02_normal107.png","imagepos/positive_triangle169.png",
    "imagepos/positive_shield44.png","imagepos/positive_shield152.png","imagepos/positive_triangle175.png","imagepos/positive_02_normal34.png",
    "imagepos/positive_02_normal118.png","imagepos/positive_02_normal104.png","imagepos/positive_triangle48.png","imagepos/positive_shield163.png",
    "imagepos/positive_02_normal46.png","imagepos/positive_triangle112.png","imagepos/positive_normal124.png","imagepos/positive_normal71.png",
    "imagepos/positive_normal102.png","imagepos/positive_triangle21.png","imagepos/positive_shield122.png","imagepos/positive_02_normal135.png",
    "imagepos/positive_02_normal175.png","imagepos/positive_shield36.png","imagepos/positive_normal72.png","imagepos/positive_02_normal171.png",
    "imagepos/positive_shield55.png","imagepos/positive_triangle141.png","imagepos/positive_02_normal188.png","imagepos/positive_triangle113.png",
    "imagepos/positive_normal5.png","imagepos/positive_02_normal99.png","imagepos/positive_triangle160.png","imagepos/positive_shield118.png",
    "imagepos/positive_normal121.png","imagepos/positive_triangle151.png","imagepos/positive_triangle59.png","imagepos/positive_shield185.png",
    "imagepos/positive_triangle154.png","imagepos/positive_shield46.png","imagepos/positive_triangle89.png","imagepos/positive_shield86.png",
    "imagepos/positive_triangle157.png","imagepos/positive_shield18.png","imagepos/positive_02_normal24.png","imagepos/positive_02_normal8.png",
    "imagepos/positive_shield22.png","imagepos/positive_normal16.png","imagepos/positive_shield157.png","imagepos/positive_triangle5.png",
    "imagepos/positive_02_normal172.png","imagepos/positive_normal178.png","imagepos/positive_02_normal151.png","imagepos/positive_triangle30.png",
    "imagepos/positive_normal19.png","imagepos/positive_normal23.png","imagepos/positive_normal47.png","imagepos/positive_triangle6.png",
    "imagepos/positive_normal130.png","imagepos/positive_02_normal187.png","imagepos/positive_shield115.png","imagepos/positive_normal7.png",
    "imagepos/positive_shield26.png","imagepos/positive_normal13.png","imagepos/positive_shield110.png","imagepos/positive_normal44.png",
    "imagepos/positive_triangle185.png","imagepos/positive_triangle163.png","imagepos/positive_shield158.png","imagepos/positive_normal15.png",
    "imagepos/positive_normal120.png","imagepos/positive_02_normal68.png","imagepos/positive_02_normal15.png","imagepos/positive_triangle64.png",
    "imagepos/positive_02_normal77.png","imagepos/positive_shield62.png","imagepos/positive_shield127.png","imagepos/positive_02_normal79.png",
    "imagepos/positive_normal38.png","imagepos/positive_normal36.png","imagepos/positive_02_normal101.png","imagepos/positive_02_normal88.png",
    "imagepos/positive_shield69.png","imagepos/positive_shield140.png","imagepos/positive_normal135.png","imagepos/positive_shield60.png",
    "imagepos/positive_02_normal9.png","imagepos/positive_normal104.png","imagepos/positive_02_normal55.png","imagepos/positive_shield89.png",
    "imagepos/positive_triangle52.png","imagepos/positive_normal134.png","imagepos/positive_02_normal117.png","imagepos/positive_shield132.png",
    "imagepos/positive_shield131.png","imagepos/positive_shield105.png","imagepos/positive_triangle168.png","imagepos/positive_normal117.png",
    "imagepos/positive_02_normal197.png","imagepos/positive_02_normal111.png","imagepos/positive_shield74.png","imagepos/positive_shield39.png",
    "imagepos/positive_shield8.png","imagepos/positive_shield109.png","imagepos/positive_02_normal134.png","imagepos/positive_triangle118.png",
    "imagepos/positive_02_normal92.png","imagepos/positive_shield17.png","imagepos/positive_normal186.png","imagepos/positive_shield119.png",
    "imagepos/positive_02_normal26.png","imagepos/positive_shield193.png","imagepos/positive_shield176.png","imagepos/positive_normal171.png",
    "imagepos/positive_triangle102.png","imagepos/positive_shield106.png","imagepos/positive_normal1.png","imagepos/positive_triangle186.png",
    "imagepos/positive_02_normal76.png"]
    horizontalDownLoopsGrp = ["loop_down_face2.png","loop_down_left_face.png","loop_down_profile1.png",
    "loop_down_right_face.png","loop_down_face.png","loop_down_left_profile1.png",
    "loop_down_profile2.png","loop_down_right_profile1.png","loop_down_left_face2.png",
    "loop_down_left_profile2.png","loop_down_right_face2.png","loop_down_right_profile2.png",
    "loop_at_very_bottom2.png","loop_at_very_bottom.png"]    
    horizontalUpLoopsGrp = ["loop_up_face2.png","loop_up_left_face.png","loop_up_profile1.png",
    "loop_up_right_face.png","loop_up_face.png","loop_up_left_profile1.png","loop_up_profile2.png",
    "loop_up_right_profile1.png","loop_up_left_face2.png","loop_up_left_profile2.png",
    "loop_up_right_face2.png","loop_up_right_profile2.png","notworking_id232_1.png"]
    verticalCenteredLoopsGrp=["loop_center_face2.png","loop_center_face.png","loop_center_profile1.png",
    "loop_center_profile2.png","loop_up_face2.png","loop_up_profile1.png","loop_up_face.png",
    "loop_up_profile2.png","loop_down_face2.png","loop_down_profile1.png","loop_down_face.png",
    "loop_down_profile2.png"]
    verticalLeftLoopsGrp=["loop_down_left_face2.png","loop_down_left_face.png","loop_down_left_profile1.png",
    "loop_down_left_profile2.png","loop_left_face2.png","loop_left_face.png","loop_left_profile1.png",
    "loop_left_profile2.png","loop_up_left_face2.png","loop_up_left_face.png","loop_up_left_profile1.png",
    "loop_up_left_profile2.png"]
    verticalRightLoopsGrp=["loop_down_right_face2.png","loop_down_right_face.png",
    "loop_down_right_profile1.png","loop_down_right_profile2.png","loop_right_face2.png","loop_right_face.png",
    "loop_right_profile1.png","loop_right_profile2.png","loop_up_right_face2.png","loop_up_right_face.png",
    "loop_up_right_profile1.png","loop_up_right_profile2.png"]

    def test_noLoops(self):
        for imgpath in self.noLoopsGrp:
            res = lucid.find_loop("sample_images/"+imgpath,zoom=0,testingProc=True)
            self.assertEqual(res[2],('No loop detected', -1, -1))

    def test_robotArm(self):
        for imgpath in self.robotArmGrp:
            res = lucid.find_loop("sample_images/"+imgpath,zoom=0,testingProc=True)
            self.assertEqual(res[2][0],'ArmRobot')
            self.assertEqual(res[2][1],res[0])

    def test_horizontalCenteredLoops(self):
        for imgpath in self.horizontalCenteredLoopsGrp:
            res = lucid.find_loop("sample_images/"+imgpath,zoom=0,testingProc=True)
            self.assertTrue(res[2][0]=='Coord' or res[2][0]=='ApproxCoord')
            self.assertTrue(((res[2][2]>((res[1]//2)-(res[1]//8))) and (res[2][2]<(res[1]//2)+(res[1]//8))))

    def test_horizontalDownLoops(self):
        for imgpath in self.horizontalDownLoopsGrp:
            res = lucid.find_loop("sample_images/"+imgpath,zoom=0,testingProc=True)
            self.assertTrue(((res[2][0]=='Coord') or (res[2][0]=='ApproxCoord')))
            self.assertTrue((res[2][2]>((res[1]//2)+(res[1]//8))))

    def test_horizontalUpLoops(self):
        for imgpath in self.horizontalUpLoopsGrp:
            res = lucid.find_loop("sample_images/"+imgpath,zoom=0,testingProc=True)
            self.assertTrue(((res[2][0]=='Coord') or (res[2][0]=='ApproxCoord')))
            self.assertTrue((res[2][2]<((res[1]//2)-(res[1]//8))))

    def test_verticalCenteredLoops(self):
        for imgpath in self.verticalCenteredLoopsGrp:
            res = lucid.find_loop("sample_images/"+imgpath,zoom=0,testingProc=True)
            self.assertTrue(((res[2][0]=='Coord') or (res[2][0]=='ApproxCoord')))
            self.assertTrue(((res[2][1]>((res[0]//2)-(res[0]//8))) and (res[2][1]<(res[0]//2)+(res[0]//8))))
    
    def test_verticalLeftLoops(self):
        for imgpath in self.verticalLeftLoopsGrp:
            res = lucid.find_loop("sample_images/"+imgpath,zoom=0,testingProc=True)
            self.assertTrue(((res[2][0]=='Coord') or (res[2][0]=='ApproxCoord')))
            self.assertTrue((res[2][1]<((res[0]//2)-(res[0]//8))))

    def test_verticalRightLoops(self):
        for imgpath in self.verticalRightLoopsGrp:
            res = lucid.find_loop("sample_images/"+imgpath,zoom=0,testingProc=True)
            self.assertTrue(((res[2][0]=='Coord') or (res[2][0]=='ApproxCoord')))
            self.assertTrue((res[2][1]>((res[0]//2)+(res[0]//8))))
            
suite = unittest.TestLoader().loadTestsFromTestCase(test)
unittest.TextTestRunner(verbosity=2).run(suite)
