package bigdata.deserializers;

import bigdata.pojo.TrafficData;
import org.apache.flink.api.common.serialization.SerializationSchema;
import com.google.gson.Gson;
import org.apache.flink.api.common.typeinfo.TypeInformation;


import java.io.Serializable;
import java.nio.charset.StandardCharsets;

public class TrafficDataSerializer implements SerializationSchema<TrafficData> {

    private static final long serialVersionUID = 1L;
    private transient Gson gson;

    @Override
    public byte[] serialize(TrafficData trafficData) {
        if (gson == null) {
            gson = new Gson();
        }
        String json = gson.toJson(trafficData);
        return json.getBytes(StandardCharsets.UTF_8);
    }

}

