package bigdata.pojo;
import com.datastax.driver.mapping.annotations.Column;
import com.datastax.driver.mapping.annotations.Table;
import java.io.Serializable;
import java.util.Date;

@Table(keyspace = "bigdata", name = "pollution")
public class PollutionData implements Serializable {

    @Column(name = "date")
    public Date Date;
    @Column(name = "laneId")
    public String LaneId;
    @Column(name = "laneCO")
    public Double LaneCO;
    @Column(name = "laneCO2")
    public Double LaneCO2;
    @Column(name = "laneHC")
    public Double LaneHC;
    @Column(name = "laneNOx")
    public Double LaneNOx;
    @Column(name = "lanePMx")
    public Double LanePMx;
    @Column(name = "laneNoise")
    public Double LaneNoise;

    public PollutionData() {

    }

    public PollutionData(java.util.Date date, String laneId, Double laneCO, Double laneCO2, Double laneHC, Double laneNOx, Double lanePMx, Double laneNoise) {
        Date = date;
        LaneId = laneId;
        LaneCO = laneCO;
        LaneCO2 = laneCO2;
        LaneHC = laneHC;
        LaneNOx = laneNOx;
        LanePMx = lanePMx;
        LaneNoise = laneNoise; 
    }

    public String getLaneId() {
        return LaneId;
    }

    public void setLaneId(String laneId) {
        LaneId = laneId;
    }

    public Double getLaneCO() {
        return LaneCO;
    }

    public void setLaneCO(Double laneCO) {
        LaneCO = laneCO;
    }

    public Double getLaneCO2() {
        return LaneCO2;
    }

    public void setLaneCO2(Double laneCO2) {
        LaneCO2 = laneCO2;
    }

    public Double getLaneHC() {
        return LaneHC;
    }

    public void setLaneHC(Double laneHC) {
        LaneHC = laneHC;
    }

    public Double getLaneNOx() {
        return LaneNOx;
    }

    public void setLaneNOx(Double laneNOx) {
        LaneNOx = laneNOx;
    }

    public Double getLanePMx() {
        return LanePMx;
    }

    public void setLanePMx(Double lanePMx) {
        LanePMx = lanePMx;
    }

    public java.util.Date getDate() {
        return Date;
    }

    public void setDate(java.util.Date date) {
        Date = date;
    }

    public Double getLaneNoise() {
        return LaneNoise;
    }

    public void setLaneNoise(Double laneNoise) {
       LaneNoise = laneNoise;
    }

    @Override
    public String toString() {
        return "LaneEmissions{" +
                "Date=" + Date +
                ", LaneId='" + LaneId + '\'' +
                ", LaneCO=" + LaneCO +
                ", LaneCO2=" + LaneCO2 +
                ", LaneHC=" + LaneHC +
                ", LaneNOx=" + LaneNOx +
                ", LanePMx=" + LanePMx +
                ", LaneNoise=" + LaneNoise +
                '}';
    }
}
