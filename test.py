import unittest
import lucid

class test(unittest.TestCase):
    noLoopsGrp = ["no_loop.png","test_id232.png"]
    horizontalCenteredLoopsGrp = ["loop_center_face2.png","loop_center_profile1.png",
    "loop_center_face.png","loop_center_profile2.png","loop_right_face2.png",
    "loop_right_profile1.png","loop_right_face.png","loop_right_profile2.png",
    "loop_right_face2.png","loop_right_profile1.png","loop_right_face.png","loop_right_profile2.png",
    "badfocus2_center_face.png","badfocus3_center_face.png","badfocus_center_face.png",
    "badfocus2_center_profile.png","badfocus3_center_profile.png","badfocus_center_profile.png",
    "tache_center_face.png","tache_center_profile.png","imagepos/positive_shield88.png"]
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
    def test_noLoops(self):
        for imgpath in self.noLoopsGrp:
            res = lucid.find_loop("/users/efrancoi/cloneGit/LUCID/lucid/sample_images/"+imgpath,zoom=0,testingProc=True)
            self.assertEqual(res[2],('No loop detected', -1, -1))

    def test_horizontalCenteredLoops(self):
        for imgpath in self.horizontalCenteredLoopsGrp:
            res = lucid.find_loop("/users/efrancoi/cloneGit/LUCID/lucid/sample_images/"+imgpath,zoom=0,testingProc=True)
            self.assertTrue(res[2][0]=='Coord' or res[2][0]=='ApproxCoord')
            self.assertTrue(((res[2][2]>((res[1]//2)-(res[1]//8))) and (res[2][2]<(res[1]//2)+(res[1]//8))))

    def test_horizontalDownLoops(self):
        for imgpath in self.horizontalDownLoopsGrp:
            res = lucid.find_loop("/users/efrancoi/cloneGit/LUCID/lucid/sample_images/"+imgpath,zoom=0,testingProc=True)
            self.assertTrue(((res[2][0]=='Coord') or (res[2][0]=='ApproxCoord')))
            self.assertTrue((res[2][2]>((res[1]//2)+(res[1]//8))))

    def test_horizontalUpLoops(self):
        for imgpath in self.horizontalUpLoopsGrp:
            res = lucid.find_loop("/users/efrancoi/cloneGit/LUCID/lucid/sample_images/"+imgpath,zoom=0,testingProc=True)
            self.assertTrue(((res[2][0]=='Coord') or (res[2][0]=='ApproxCoord')))
            self.assertTrue((res[2][2]<((res[1]//2)-(res[1]//8))))

    def test_verticalCenteredLoops(self):
        for imgpath in self.verticalCenteredLoopsGrp:
            res = lucid.find_loop("/users/efrancoi/cloneGit/LUCID/lucid/sample_images/"+imgpath,zoom=0,testingProc=True)
            self.assertTrue(((res[2][0]=='Coord') or (res[2][0]=='ApproxCoord')))
            self.assertTrue(((res[2][1]>((res[0]//2)-(res[0]//8))) and (res[2][1]<(res[0]//2)+(res[0]//8))))
            
suite = unittest.TestLoader().loadTestsFromTestCase(test)
unittest.TextTestRunner(verbosity=2).run(suite)
