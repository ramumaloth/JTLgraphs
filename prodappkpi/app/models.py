from django.db import models


class ProdAppKPiModel(models.Model):
    timeStamp= models.CharField(max_length=100)
    elapsed = models.CharField(max_length=100)
    label= models.CharField(max_length=100)
    responseCode= models.CharField(max_length=100)
    responseMessage = models.CharField(max_length=100)
    threadName=models.CharField(max_length=100)
    dataType= models.CharField(max_length=100)
    success=models.CharField(max_length=100)
    failureMessage=models.CharField(max_length=100)
    bytes= models.CharField(max_length=100)
    sentBytes=models.CharField(max_length=100)
    grpThreads =models.CharField(max_length=100)
    allThreads=models.CharField(max_length=100)
    URL=models.CharField(max_length=100)
    Latency=models.CharField(max_length=100)
    IdleTime=models.CharField(max_length=100)
    Connect=models.CharField(max_length=100)

    def __str__(self):
        return self.timeStamp

    class Meta:
        db_table = 'perfresults'


