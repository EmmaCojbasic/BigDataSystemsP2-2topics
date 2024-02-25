package bigdata.pojo;

import com.google.gson.annotations.SerializedName;

public class VehicleInfo {          // DONE

    @SerializedName("timestep_time")
    public Double TimeStep;
    @SerializedName("vehicle_angle")
    public Double VehicleAngle;
    @SerializedName("vehicle_id")
    public int VehicleId;
    @SerializedName("vehicle_lane")
    public String VehicleLane;
    @SerializedName("vehicle_pos")
    public Double VehiclePos;
    @SerializedName("vehicle_slope")
    public Double VehicleSlope;
    @SerializedName("vehicle_speed")
    public Double VehicleSpeed;
    @SerializedName("vehicle_type")
    public String VehicleType;
    @SerializedName("vehicle_x")
    public Double VehicleX;
    @SerializedName("vehicle_y")
    public Double VehicleY;

    // Default constructor
    public VehicleInfo() {}

    // Constructor with parameters
    public VehicleInfo(Double timeStep, Double vehicleAngle, int vehicleId, String vehicleLane,
                       Double vehiclePos, Double vehicleSlope, Double vehicleSpeed,
                       String vehicleType, Double vehicleX, Double vehicleY) {
        TimeStep = timeStep;
        VehicleAngle = vehicleAngle;
        VehicleId = vehicleId;
        VehicleLane = vehicleLane;
        VehiclePos = vehiclePos;
        VehicleSlope = vehicleSlope;
        VehicleSpeed = vehicleSpeed;
        VehicleType = vehicleType;
        VehicleX = vehicleX;
        VehicleY = vehicleY;
    }

    public Double getTimeStep() {
        return TimeStep;
    }

    public void setTimeStep(Double timeStep) {
        TimeStep = timeStep;
    }

    public Double getVehicleAngle() {
        return VehicleAngle;
    }

    public void setVehicleAngle(Double vehicleAngle) {
        VehicleAngle = vehicleAngle;
    }

    public int getVehicleId() {
        return VehicleId;
    }

    public void setVehicleId(int vehicleId) {
        VehicleId = vehicleId;
    }

    public String getVehicleLane() {
        return VehicleLane;
    }

    public void setVehicleLane(String vehicleLane) {
        VehicleLane = vehicleLane;
    }

    public Double getVehiclePos() {
        return VehiclePos;
    }

    public void setVehiclePos(Double vehiclePos) {
        VehiclePos = vehiclePos;
    }

    public Double getVehicleSlope() {
        return VehicleSlope;
    }

    public void setVehicleSlope(Double vehicleSlope) {
        VehicleSlope = vehicleSlope;
    }

    public Double getVehicleSpeed() {
        return VehicleSpeed;
    }

    public void setVehicleSpeed(Double vehicleSpeed) {
        VehicleSpeed = vehicleSpeed;
    }

    public String getVehicleType() {
        return VehicleType;
    }

    public void setVehicleType(String vehicleType) {
        VehicleType = vehicleType;
    }

    public Double getVehicleX() {
        return VehicleX;
    }

    public void setVehicleX(Double vehicleX) {
        VehicleX = vehicleX;
    }

    public Double getVehicleY() {
        return VehicleY;
    }

    public void setVehicleY(Double vehicleY) {
        VehicleY = vehicleY;
    }
}
