package bigdata.analytics;

import bigdata.deserializers.*;
import bigdata.pojo.*;
import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;

import java.util.Date;

public class LaneAggregator extends ProcessWindowFunction<EmissionInfo, PollutionData, String, TimeWindow> {

    @Override
    public void process(String key, Context context, Iterable<EmissionInfo> emissions, Collector<PollutionData> out) throws Exception {

        double totalCO = 0.0;
        double totalCO2 = 0.0;
        double totalHC = 0.0;
        double totalNOx = 0.0;
        double totalPMx = 0.0;
        double totalNoise = 0.0;

        for (EmissionInfo e : emissions) {
            totalCO += e.VehicleCO;
            totalCO2 += e.VehicleCO2;
            totalHC += e.VehicleHC;
            totalNOx += e.VehicleNOx;
            totalPMx += e.VehiclePMx;
            totalNoise += e.VehicleNoise;
        }

        out.collect(new PollutionData(new Date(), key, totalCO, totalCO2, totalHC, totalNOx, totalPMx, totalNoise));
    }
}

