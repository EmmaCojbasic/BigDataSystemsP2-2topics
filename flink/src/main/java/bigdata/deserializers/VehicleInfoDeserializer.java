package bigdata.deserializers;

import bigdata.deserializers.*;
import bigdata.pojo.*;
import org.apache.flink.api.common.serialization.DeserializationSchema;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import com.google.gson.Gson;
import java.io.IOException;
import java.nio.charset.StandardCharsets;

public class VehicleInfoDeserializer implements DeserializationSchema<VehicleInfo> {

    private static final long serialVersionUID = 1L;

    @Override
    public VehicleInfo deserialize(byte[] bytes) throws IOException {
        String json = new String(bytes, StandardCharsets.UTF_8);
        Gson gson = new Gson();
        return gson.fromJson(json, VehicleInfo.class);
    }

    @Override
    public boolean isEndOfStream(VehicleInfo vehicleInfo) {
        return false;
    }

    @Override
    public TypeInformation<VehicleInfo> getProducedType() {
        return TypeInformation.of(VehicleInfo.class);
    }
}