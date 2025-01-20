class BinaryConfusionMatrix:
    def __init__(self, pos_tag, neg_tag):
        self.pos_tag = pos_tag
        self.neg_tag = neg_tag
        self.tp =0
        self.tn =0
        self.fp =0
        self.fn =0

    def as_dict(self):
        return {'tp':self.tp, 'tn':self.tn, 'fp':self.fp, 'fn':self.fn}

    def update(self,truth, prediction):
        if truth not in (self.pos_tag,self.neg_tag):
            raise ValueError('The parameters can be either %s or %s' %(self.pos_tag, self.neg_tag))
        if prediction not in (self.pos_tag,self.neg_tag):
            raise ValueError('The parameters can be either %s or %s' %(self.pos_tag, self.neg_tag))

        if prediction == self.pos_tag:
            if truth==prediction:
                self.tp+=1
            else:
                self.fp +=1
        elif prediction ==self.neg_tag:
            if truth == prediction:
                self.tn +=1
            else:
                self.fn +=1

    def compute_from_dicts(self, truth_dict, pred_dict):
        for key in truth_dict:
            self.update(truth_dict[key], pred_dict[key])
